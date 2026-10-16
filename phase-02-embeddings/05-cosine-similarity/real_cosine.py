import numpy as np
from dotenv import load_dotenv
from openai import OpenAI

EMBEDDING_MODEL = "text-embedding-3-small"

load_dotenv()
client = OpenAI(timeout=60, max_retries=2)


def embed(text):
    response = client.embeddings.create(model=EMBEDDING_MODEL, input=text)
    return np.array(response.data[0].embedding, dtype=np.float32)


def cosine_scores(matrix, query):
    return (matrix @ query) / (np.linalg.norm(matrix, axis=1) * np.linalg.norm(query))


query = "How do I reset my password?"
documents = [
    "I forgot my login password and need to change it.",   # same meaning, different words
    "How can I change the email address on my account?",   # same topic area (account settings)
    "Where can I download my monthly invoice?",            # same app, different task
    "The app crashes when I open the settings page.",      # support, but a bug report
    "What is the capital of France?",                      # unrelated
]

query_vector = embed(query)
document_matrix = np.array([embed(text) for text in documents])

cosines = cosine_scores(document_matrix, query_vector)
dots = document_matrix @ query_vector

print(f"Query: {query!r}\n")
print(f"   {'cosine':>7}  {'dot':>7}  document")
for index in np.argsort(-cosines):
    print(f"   {cosines[index]:7.4f}  {dots[index]:7.4f}  {documents[index]}")

print(f"\nLargest |cosine - dot| across all documents: {np.max(np.abs(cosines - dots)):.6f}")
