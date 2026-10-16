import numpy as np
from dotenv import load_dotenv
from openai import OpenAI

EMBEDDING_MODEL = "text-embedding-3-small"

load_dotenv()
client = OpenAI(timeout=60, max_retries=2)


def embed(text):
    response = client.embeddings.create(model=EMBEDDING_MODEL, input=text)
    return np.array(response.data[0].embedding, dtype=np.float32)


query = "How do I reset my password?"
documents = [
    "I forgot my login password and need to change it.",
    "Where can I download my monthly invoice?",
    "What is the capital of France?",
]

query_vector = embed(query)
document_matrix = np.array([embed(text) for text in documents])

print(f"Query: {query!r}")
print(f"Query norm: {np.linalg.norm(query_vector):.4f}")
print(f"Matrix shape: {document_matrix.shape}\n")

scores = document_matrix @ query_vector
for text, score in sorted(zip(documents, scores), key=lambda pair: pair[1], reverse=True):
    print(f"   {score:.4f}  {text}")
