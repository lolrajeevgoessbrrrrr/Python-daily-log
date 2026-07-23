import os
import requests
import json
from dotenv import load_dotenv
import anthropic
from groq import Groq

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

claude_client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
groq_client = Groq(api_key=GROQ_API_KEY)


def search_web(query):
    url = "https://api.tavily.com/search"
    payload = {
        "api_key": TAVILY_API_KEY,
        "query": query,
        "max_results": 3
    }
    response = requests.post(url, json=payload)
    data = response.json()
    results = data.get("results", [])

    formatted_results = ""
    result_number = 1
    for result in results:
        title = result.get("title", "No title")
        content = result.get("content", "No summary available")
        formatted_results = formatted_results + str(result_number) + ". " + title + "\n"
        formatted_results = formatted_results + content + "\n\n"
        result_number = result_number + 1

    return formatted_results


search_tool_schema_claude = {
    "name": "search_web",
    "description": "Search the internet for current information, facts, news, or anything you are unsure about or that might have changed recently.",
    "input_schema": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The exact search query to look up"
            }
        },
        "required": ["query"]
    }
}

search_tool_schema_groq = {
    "type": "function",
    "function": {
        "name": "search_web",
        "description": "Search the internet for current information, facts, news, or anything you are unsure about or that might have changed recently.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The exact search query to look up"
                }
            },
            "required": ["query"]
        }
    }
}


def ask_agent_claude(user_question):
    messages = [
        {"role": "user", "content": user_question}
    ]

    response = claude_client.messages.create(
        model="claude-sonnet-5",
        max_tokens=1024,
        tools=[search_tool_schema_claude],
        messages=messages
    )

    if response.stop_reason != "tool_use":
        answer = ""
        for block in response.content:
            if block.type == "text":
                answer = answer + block.text
        return answer

    tool_use_block = None
    for block in response.content:
        if block.type == "tool_use":
            tool_use_block = block

    search_query = tool_use_block.input["query"]
    print("Claude wants to search for:", search_query)
    search_results = search_web(search_query)

    messages.append({"role": "assistant", "content": response.content})
    messages.append({
        "role": "user",
        "content": [
            {
                "type": "tool_result",
                "tool_use_id": tool_use_block.id,
                "content": search_results
            }
        ]
    })

    final_response = claude_client.messages.create(
        model="claude-sonnet-5",
        max_tokens=1024,
        tools=[search_tool_schema_claude],
        messages=messages
    )

    final_answer = ""
    for block in final_response.content:
        if block.type == "text":
            final_answer = final_answer + block.text

    return final_answer


def ask_agent_groq(user_question):
    messages = [
        {"role": "user", "content": user_question}
    ]

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=1024,
        tools=[search_tool_schema_groq],
        messages=messages
    )

    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls

    if not tool_calls:
        return response_message.content

    tool_call = tool_calls[0]
    arguments = json.loads(tool_call.function.arguments)
    search_query = arguments["query"]
    print("Groq wants to search for:", search_query)
    search_results = search_web(search_query)

    assistant_message = {
        "role": "assistant",
        "content": response_message.content,
        "tool_calls": [
            {
                "id": tool_call.id,
                "type": "function",
                "function": {
                    "name": tool_call.function.name,
                    "arguments": tool_call.function.arguments
                }
            }
        ]
    }
    messages.append(assistant_message)

    messages.append({
        "role": "tool",
        "tool_call_id": tool_call.id,
        "name": "search_web",
        "content": search_results
    })

    final_response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=1024,
        tools=[search_tool_schema_groq],
        messages=messages
    )

    final_answer = final_response.choices[0].message.content
    return final_answer


if __name__ == "__main__":
    provider = input("Which model do you want to use? Type 'groq' or 'claude': ")
    provider = provider.lower()

    print("Ask me anything. I can search the web now. Type 'quit' to exit.")
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == "quit":
            break

        if provider == "claude":
            answer = ask_agent_claude(user_input)
        else:
            answer = ask_agent_groq(user_input)

        print("\nAgent:", answer)