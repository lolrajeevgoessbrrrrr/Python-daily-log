import os
import logging
import anthropic
import groq
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="day29.log",
    filemode="a"
)

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = "You are a helpful and concise coding assistant. Give clear, practical answers with short code examples when needed."

CLAUDE_MODEL = "claude-haiku-4-5-20251001"
GROQ_MODEL = "openai/gpt-oss-120b"


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
        logger.info("Anthropic client created successfully")

    else:
        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError("GROQ_API_KEY missing. Check your .env file.")

        client = groq.Groq(api_key=api_key)
        logger.info("Groq client created successfully")

    return client


def stream_reply(provider, client, conversation_history):
    full_reply = ""
    input_tokens = 0
    output_tokens = 0

    print(f"\n{provider.capitalize()}: ", end="", flush=True)

    if provider == "claude":
        with client.messages.stream(
            model=CLAUDE_MODEL,
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            messages=conversation_history
        ) as stream:

            for text_piece in stream.text_stream:
                print(text_piece, end="", flush=True)
                full_reply = full_reply + text_piece

            final_message = stream.get_final_message()
            input_tokens = final_message.usage.input_tokens
            output_tokens = final_message.usage.output_tokens

    else:
        groq_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + conversation_history

        stream = client.chat.completions.create(
            model=GROQ_MODEL,
            max_tokens=1024,
            messages=groq_messages,
            stream=True,
            stream_options={"include_usage": True}
        )

        for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                piece = chunk.choices[0].delta.content
                print(piece, end="", flush=True)
                full_reply = full_reply + piece

            if chunk.usage:
                input_tokens = chunk.usage.prompt_tokens
                output_tokens = chunk.usage.completion_tokens

    print("\n")

    logger.info(f"Reply received. Tokens — in: {input_tokens}, out: {output_tokens}")

    return full_reply, input_tokens, output_tokens


def add_message(conversation_history, role, text):
    new_message = {
        "role": role,
        "content": text
    }

    conversation_history.append(new_message)

    return conversation_history


def show_history(conversation_history):
    print("\n--- Conversation History ---")

    for index, message in enumerate(conversation_history):
        role = message["role"].upper()
        content = message["content"]

        if len(content) > 100:
            content = content[:100] + "..."

        print(f"[{index + 1}] {role}: {content}")

    print("----------------------------\n")


def run():
    print("=== Day 29: Claude/Groq API — Streaming + Multi-Turn ===")
    print("Commands: 'quit' | 'history' | 'clear'\n")

    provider = choose_provider()
    client = create_client(provider)

    conversation_history = []
    total_input_tokens = 0
    total_output_tokens = 0

    while True:
        user_input = input("You: ").strip()

        if user_input == "":
            print("Type something!\n")
            continue

        if user_input.lower() == "quit":
            print(f"\nSession ended. Total tokens → Input: {total_input_tokens} | Output: {total_output_tokens}")
            logger.info(f"Session ended. In: {total_input_tokens}, Out: {total_output_tokens}")
            break

        if user_input.lower() == "history":
            show_history(conversation_history)
            continue

        if user_input.lower() == "clear":
            conversation_history = []
            total_input_tokens = 0
            total_output_tokens = 0
            print("Conversation cleared!\n")
            logger.info("Conversation cleared")
            continue

        conversation_history = add_message(conversation_history, "user", user_input)

        try:
            reply, in_tokens, out_tokens = stream_reply(provider, client, conversation_history)

            conversation_history = add_message(conversation_history, "assistant", reply)

            total_input_tokens = total_input_tokens + in_tokens
            total_output_tokens = total_output_tokens + out_tokens

        except (anthropic.APIConnectionError, groq.APIConnectionError) as e:
            print(f"\nConnection error: {e}\n")
            logger.error(f"Connection error: {e}")
            conversation_history.pop()

        except (anthropic.RateLimitError, groq.RateLimitError) as e:
            print(f"\nRate limit hit. Wait a moment.\n")
            logger.error(f"Rate limit: {e}")
            conversation_history.pop()

        except (anthropic.APIStatusError, groq.APIStatusError) as e:
            print(f"\nAPI error: {e}\n")
            logger.error(f"Status error: {e}")
            conversation_history.pop()


if __name__ == "__main__":
    run()