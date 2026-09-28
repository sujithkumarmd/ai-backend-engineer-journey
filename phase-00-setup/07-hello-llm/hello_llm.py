from dotenv import load_dotenv
from openai import OpenAI

MODEL = "gpt-6-luna"

load_dotenv()

client = OpenAI()

response = client.responses.create(
    model=MODEL,
    input="Hello",
)

print(response.output_text)
