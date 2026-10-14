from dotenv import load_dotenv
from openai import OpenAI

EMBEDDING_MODEL = "text-embedding-3-small"
PRICE_PER_TOKEN = 0.02 / 1_000_000   # $0.02 per 1M tokens, checked 12 Oct 2026

load_dotenv()
client = OpenAI(timeout=60, max_retries=2)


def embed(text):
    response = client.embeddings.create(model=EMBEDDING_MODEL, input=text)
    return response.data[0].embedding, response.usage.total_tokens


texts = [
    "How do I reset my password?",
    "I forgot my login password and need to change it.",
    "What is the capital of France?",
    "Hi",
]

total_tokens = 0
for text in texts:
    vector, tokens = embed(text)
    total_tokens += tokens
    first_five = [round(number, 4) for number in vector[:5]]
    print(f"{text!r}")
    print(f"   {len(vector)} numbers · {tokens} tokens · starts with {first_five}\n")

print(f"Total: {total_tokens} tokens = ${total_tokens * PRICE_PER_TOKEN:.8f}")

# Same text twice: do we get the same vector?
first, _ = embed("Hi")
second, _ = embed("Hi")
biggest_difference = max(abs(a - b) for a, b in zip(first, second))
print(f"Same text embedded twice, biggest difference in any position: {biggest_difference:.8f}")
