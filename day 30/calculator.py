import os
import json
import logging
import datetime
import requests
import anthropic
import groq
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="day30.log",
    filemode="a"
)

logger = logging.getLogger(__name__)

CLAUDE_MODEL = "claude-haiku-4-5-20251001"
GROQ_MODEL = "openai/gpt-oss-120b"

# Tool definitions in Anthropic's format
TOOLS_CLAUDE = [
    {
        "name": "get_current_time",
        "description": "Returns the current date and time. Use when the user asks what time or date it is.",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "calculate",
        "description": "Evaluates a math expression and returns the result. Use for any arithmetic calculation.",
        "input_schema": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "A math expression like '15 * 4' or '(100 + 50) / 3'"
                }
            },
            "required": ["expression"]
        }
    },
    {
        "name": "get_dad_joke",
        "description": "Fetches a random dad joke from the internet. Use when the user asks for a joke.",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
]

# Same three tools in Groq's (OpenAI-style) format
TOOLS_GROQ = [
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "Returns the current date and time. Use when the user asks what time or date it is.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Evaluates a math expression and returns the result. Use for any arithmetic calculation.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "A math expression like '15 * 4' or '(100 + 50) / 3'"
                    }
                },
                "required": ["expression"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_dad_joke",
            "description": "Fetches a random dad joke from the internet. Use when the user asks for a joke.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    }
]


# Tool function 1: returns current date and time
def get_current_time():
    now = datetime.datetime.now()
    formatted = now.strftime("%A, %B %d %Y at %I:%M %p")
    return formatted


# Tool function 2: safely evaluates a math expression
def calculate(expression):
    allowed_chars = set("0123456789+-*/()., ")
    expression_chars = set(expression)

    has_unsafe_char = not expression_chars.issubset(allowed_chars)

    if has_unsafe_char:
        return "Error: Only basic math operators allowed."

    try:
        result = eval(expression)
        result_str = str(result)
        return result_str
    except Exception as calc_error:
        return f"Error: {calc_error}"


# Tool function 3: fetches a random dad joke from the internet
def get_dad_joke():
    try:
        headers = {"Accept": "application/json"}
        response = requests.get("https://icanhazdadjoke.com/", headers=headers)

        if response.status_code == 200:
            data = response.json()
            joke = data["joke"]
            return joke
        else:
            return "Couldn't fetch a joke right now."

    except Exception as joke_error:
        return f"Error fetching joke: {joke_error}"


# Dispatcher: decides which real function to run based on what the model asked for
def run_tool(tool_name, tool_input):
    logger.info(f"Tool called: {tool_name} | Input: {tool_input}")

    if tool_name == "get_current_time":
        result = get_current_time()

    elif tool_name == "calculate":
        expression = tool_input["expression"]
        result = calculate(expression)

    elif tool_name == "get_dad_joke":
        result = get_dad_joke()

    else:
        result = f"Unknown tool: {tool_name}"

    logger.info(f"Tool result: {result}")

    return result


def choose_provider():
    while True:
        choice = input("Use Claude API or Groq API? (claude/groq): ").strip().lower()

        if choice in ("claude", "groq"):
            return choice

        print("Please type 'claude' or 'groq'.\n")


def create_client(provider):
    if provider == "claude":
        api_key = os.getenv("ANTHROPIC_API_KEY")

        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY missing. Check your .env file.")

        client = anthropic.Anthropic(api_key=api_key)
        logger.info("Anthropic client created")

    else:
        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError("GROQ_API_KEY missing. Check your .env file.")

        client = groq.Groq(api_key=api_key)
        logger.info("Groq client created")

    return client


def send_to_model(provider, client, messages):
    if provider == "claude":
        response = client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=1024,
            tools=TOOLS_CLAUDE,
            messages=messages
        )

    else:
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            max_tokens=1024,
            tools=TOOLS_GROQ,
            messages=messages
        )

    return response


def handle_response_claude(client, messages, response):

    # Case 1: Claude wants to use a tool before answering
    if response.stop_reason == "tool_use":

        # Add Claude's response (which contains its tool request) to history
        messages.append({
            "role": "assistant",
            "content": response.content
        })

        # Build a list of tool results to send back
        tool_results = []

        for block in response.content:

            if block.type == "tool_use":
                tool_name = block.name
                tool_input = block.input
                tool_id = block.id

                print(f"\n  [Tool used: {tool_name}]")

                # Actually run the Python function
                result = run_tool(tool_name, tool_input)

                # Package the result in the format Claude expects
                result_block = {
                    "type": "tool_result",
                    "tool_use_id": tool_id,
                    "content": result
                }

                tool_results.append(result_block)

        # Send tool results back to Claude as a user message
        messages.append({
            "role": "user",
            "content": tool_results
        })

        # Now ask Claude to give a final answer using the tool data
        follow_up = send_to_model("claude", client, messages)

        # Extract the final text reply
        final_text = ""
        for block in follow_up.content:
            if hasattr(block, "text"):
                final_text = final_text + block.text

        # Add Claude's final reply to history
        messages.append({
            "role": "assistant",
            "content": final_text
        })

        print(f"\nClaude: {final_text}\n")

    # Case 2: Claude answered directly without using any tool
    else:
        reply_text = ""
        for block in response.content:
            if hasattr(block, "text"):
                reply_text = reply_text + block.text

        messages.append({
            "role": "assistant",
            "content": reply_text
        })

        print(f"\nClaude: {reply_text}\n")

    return messages


def handle_response_groq(client, messages, response):
    choice = response.choices[0]
    groq_message = choice.message

    # Case 1: Groq wants to use a tool before answering
    if choice.finish_reason == "tool_calls" and groq_message.tool_calls:

        tool_call_dicts = []
        for tool_call in groq_message.tool_calls:
            tool_call_dicts.append({
                "id": tool_call.id,
                "type": "function",
                "function": {
                    "name": tool_call.function.name,
                    "arguments": tool_call.function.arguments
                }
            })

        # Add the assistant's tool request to history
        messages.append({
            "role": "assistant",
            "content": groq_message.content,
            "tool_calls": tool_call_dicts
        })

        for tool_call in groq_message.tool_calls:
            tool_name = tool_call.function.name
            tool_input = json.loads(tool_call.function.arguments)
            tool_id = tool_call.id

            print(f"\n  [Tool used: {tool_name}]")

            # Actually run the Python function
            result = run_tool(tool_name, tool_input)

            # Package the result in the format Groq expects
            messages.append({
                "role": "tool",
                "tool_call_id": tool_id,
                "content": result
            })

        # Now ask Groq to give a final answer using the tool data
        follow_up = send_to_model("groq", client, messages)
        final_text = follow_up.choices[0].message.content or ""

        # Add the final reply to history
        messages.append({
            "role": "assistant",
            "content": final_text
        })

        print(f"\nGroq: {final_text}\n")

    # Case 2: Groq answered directly without using any tool
    else:
        reply_text = groq_message.content or ""

        messages.append({
            "role": "assistant",
            "content": reply_text
        })

        print(f"\nGroq: {reply_text}\n")

    return messages


def handle_response(provider, client, messages, response):
    if provider == "claude":
        return handle_response_claude(client, messages, response)
    else:
        return handle_response_groq(client, messages, response)


def run():
    print("=== Day 30: Claude/Groq API — Tool Use ===")
    print("Try: 'What time is it?' | 'Calculate 247 * 18' | 'Tell me a joke'")
    print("Type 'quit' to exit\n")

    provider = choose_provider()
    client = create_client(provider)
    messages = []

    while True:
        user_input = input("You: ").strip()

        if user_input == "":
            print("Say something!\n")
            continue

        if user_input.lower() == "quit":
            print("Goodbye!")
            logger.info("Session ended")
            break

        messages.append({
            "role": "user",
            "content": user_input
        })

        try:
            response = send_to_model(provider, client, messages)
            messages = handle_response(provider, client, messages, response)

        except (anthropic.APIConnectionError, groq.APIConnectionError) as e:
            print(f"\nConnection error: {e}\n")
            logger.error(f"Connection error: {e}")
            messages.pop()

        except (anthropic.RateLimitError, groq.RateLimitError) as e:
            print(f"\nRate limit hit. Wait a moment.\n")
            logger.error(f"Rate limit: {e}")
            messages.pop()

        except (anthropic.APIStatusError, groq.APIStatusError) as e:
            print(f"\nAPI error: {e}\n")
            logger.error(f"Status error: {e}")
            messages.pop()


if __name__ == "__main__":
    run()