import os
import requests
import json
import logging
from dotenv import load_dotenv
import anthropic
from groq import Groq

load_dotenv()

logging.basicConfig(
    filename="search_agent.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

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

    try:
        response = requests.post(url, json=payload, timeout=10)
        data = response.json()
    except requests.exceptions.RequestException as error:
        logging.error("Search request failed: " + str(error))
        return "Search failed. Could not reach the internet right now."

    results = data.get("results", [])
    formatted_results = ""
    result_number = 1
    for result in results:
        title = result.get("title", "No title")
        content = result.get("content", "No summary available")
        formatted_results = formatted_results + str(result_number) + ". " + title + "\n"
        formatted_results = formatted_results + content + "\n\n"
        result_number = result_number + 1

    logging.info("Searched for: " + query)
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


def run_agent_turn_claude(messages):
    max_iterations = 5
    current_iteration = 0

    while current_iteration < max_iterations:
        response = claude_client.messages.create(
            model="claude-sonnet-5",
            max_tokens=1024,
            tools=[search_tool_schema_claude],
            messages=messages
        )

        if response.stop_reason != "tool_use":
            final_answer = ""
            for block in response.content:
                if block.type == "text":
                    final_answer = final_answer + block.text
            messages.append({"role": "assistant", "content": response.content})
            return final_answer, messages

        tool_use_block = None
        for block in response.content:
            if block.type == "tool_use":
                tool_use_block = block

        search_query = tool_use_block.input["query"]
        print("Searching:", search_query)
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

        current_iteration = current_iteration + 1

    return "Reached the search limit for this question.", messages


def run_agent_turn_groq(messages):
    max_iterations = 5
    current_iteration = 0

    while current_iteration < max_iterations:
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            max_tokens=1024,
            tools=[search_tool_schema_groq],
            messages=messages
        )

        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls

        if not tool_calls:
            messages.append({
                "role": "assistant",
                "content": response_message.content
            })
            return response_message.content, messages

        tool_call = tool_calls[0]
        arguments = json.loads(tool_call.function.arguments)
        search_query = arguments["query"]
        print("Searching:", search_query)
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

        current_iteration = current_iteration + 1

    return "Reached the search limit for this question.", messages


if __name__ == "__main__":
    provider = input("Which model do you want to use? Type 'groq' or 'claude': ")
    provider = provider.lower()

    print("Agent ready. I remember our conversation and can search multiple times if needed.")
    conversation_history = []

    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == "quit":
            break

        conversation_history.append({"role": "user", "content": user_input})

        if provider == "claude":
            answer, conversation_history = run_agent_turn_claude(conversation_history)
        else:
            answer, conversation_history = run_agent_turn_groq(conversation_history)

        print("\nAgent:", answer)