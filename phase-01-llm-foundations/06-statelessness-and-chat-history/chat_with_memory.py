from dotenv import load_dotenv
from openai import OpenAI

MODEL = "gpt-6-luna"

load_dotenv()
client = OpenAI(timeout=60, max_retries=2)

messages = [
    {"role": "developer", "content": "You are a friendly assistant. Keep answers under 3 sentences."},
]

print("Chat started. Type 'quit' to exit.\n")

while True:
    user_text = input("You: ").strip()
    if user_text.lower() in {"quit", "exit"}:
        break
    if not user_text:
        continue

    messages.append({"role": "user", "content": user_text})
    sent_count = len(messages)

    response = client.responses.create(model=MODEL, input=messages)
    reply = response.output_text

    messages.append({"role": "assistant", "content": reply})

    print(f"AI: {reply}\n")

    print(f"Messages: {messages}\n")
    print(f"    [sent {sent_count} messages · input tokens this turn: {response.usage.input_tokens}]\n")

print(f"Bye! The conversation had {len(messages)} messages.")
