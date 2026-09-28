from openai import OpenAI
from dotenv import load_dotenv


MODEL = "gpt-6-luna"

load_dotenv()
client = OpenAI()

response = client.responses.create(
    model=MODEL,
    input = "Hi"
)

print("AI response: ", response.output_text)