import openai
import tiktoken
from dotenv import load_dotenv
from openai import OpenAI

from cost_calculator import calculate_cost

MODEL = "gpt-6-luna"
REASONING_EFFORT = "low"
MAX_OUTPUT_TOKENS = 600   # safety net: reasoning + reply (a 4-sentence answer is ~100 tokens)
HISTORY_TOKEN_BUDGET = 2000   # most input tokens we are willing to send per message (a cost choice)
DEVELOPER_PROMPT = (
    "You are a friendly, concise assistant. "
    "Keep answers under 4 sentences unless the user asks for more detail."
)
HELP_TEXT = """    Commands:
      /stats  show tokens and cost so far
      /reset  clear the conversation memory (totals are kept)
      /help   show this list
      /quit   exit
"""

load_dotenv()
client = OpenAI(timeout=60, max_retries=2)
encoding = tiktoken.get_encoding("o200k_base")


def count_tokens(messages):
    return sum(len(encoding.encode(message["content"])) for message in messages)


def trim_history(messages):
    developer, history = messages[0], messages[1:]
    dropped = 0
    while len(history) > 1 and count_tokens([developer] + history) > HISTORY_TOKEN_BUDGET:
        history = history[2:]
        dropped += 2
    return [developer] + history, dropped


def get_reply(messages):
    response = client.responses.create(
        model=MODEL,
        input=messages,
        reasoning={"effort": REASONING_EFFORT},
        max_output_tokens=MAX_OUTPUT_TOKENS,
    )

    warning = None
    if response.status != "completed":
        reason = response.incomplete_details.reason if response.incomplete_details else "unknown"
        warning = f"Reply was cut off ({reason})."

    return response.output_text, response.usage, warning


def describe_error(error):
    if isinstance(error, openai.APIConnectionError):
        return "Could not reach OpenAI (network problem or timeout)."
    if isinstance(error, openai.RateLimitError):
        if error.code == "rate_limit_exceeded":
            return "Sending too fast (rate limit). Wait a few seconds."
        return f"Quota or spend limit reached ({error.code}). This needs fixing in the OpenAI dashboard."
    if isinstance(error, openai.AuthenticationError):
        return "The API key was rejected. Check AI-claude/.env."
    return f"API error: {error.message}"


def new_conversation():
    return [{"role": "developer", "content": DEVELOPER_PROMPT}]


def print_stats(stats, messages):
    print(f"    📊 turns: {stats['turns']} · messages in memory: {len(messages) - 1} "
          f"(~{count_tokens(messages)} tokens)")
    print(f"       tokens in: {stats['input_tokens']} · out: {stats['output_tokens']} · "
          f"cost: ${stats['cost']:.6f}\n")


def main():
    messages = new_conversation()
    stats = {"turns": 0, "input_tokens": 0, "output_tokens": 0, "cost": 0.0}

    print(f"Chatbot ready ({MODEL}, effort={REASONING_EFFORT}). Type /help for commands.\n")

    while True:
        user_text = input("You: ").strip()
        if not user_text:
            continue

        if user_text.lower() in {"/quit", "/exit", "quit", "exit"}:
            break

        if user_text.startswith("/"):
            command = user_text.lower()
            if command == "/stats":
                print_stats(stats, messages)
            elif command == "/reset":
                messages = new_conversation()
                print("    🧹 Conversation memory cleared. Session totals are kept.\n")
            elif command == "/help":
                print(HELP_TEXT)
            else:
                print(f"    Unknown command {command!r}. Type /help.\n")
            continue

        messages.append({"role": "user", "content": user_text})
        to_send, dropped = trim_history(messages)
        try:
            reply, usage, warning = get_reply(to_send)
        except openai.APIError as error:
            messages.pop()
            print(f"    ❌ {describe_error(error)} Your message was not sent; try again.\n")
            continue
        messages.append({"role": "assistant", "content": reply})

        cost = calculate_cost(
            MODEL,
            usage.input_tokens,
            usage.output_tokens,
            usage.input_tokens_details.cached_tokens,
        )
        stats["turns"] += 1
        stats["input_tokens"] += usage.input_tokens
        stats["output_tokens"] += usage.output_tokens
        stats["cost"] += cost

        print(f"AI: {reply}")
        if warning:
            print(f"    ⚠️ {warning}")
        if dropped:
            print(f"    ✂️ Oldest {dropped} messages were not sent (budget: {HISTORY_TOKEN_BUDGET} tokens)")
        print(f"    [in {usage.input_tokens} · out {usage.output_tokens} · "
              f"this message ${cost:.6f} · session ${stats['cost']:.6f}]\n")

    print("\nSession summary")
    print_stats(stats, messages)
    if stats["turns"]:
        print(f"    Average cost per turn: ${stats['cost'] / stats['turns']:.6f}")
    print("Bye!")


if __name__ == "__main__":
    main()
