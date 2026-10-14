from dotenv import load_dotenv
from openai import OpenAI

EMBEDDING_MODEL = "text-embedding-3-small"
TEXT = "How do I reset my password?"

load_dotenv()
client = OpenAI(timeout=60, max_retries=2)

for dimensions in [1536, 512, 256]:
    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=TEXT,
        dimensions=dimensions,
    )
    vector = response.data[0].embedding
    print(f"asked for {dimensions:>4} → got {len(vector):>4} numbers · "
          f"{response.usage.total_tokens} tokens · "
          f"storage at 4 bytes each: {len(vector) * 4:,} bytes")
