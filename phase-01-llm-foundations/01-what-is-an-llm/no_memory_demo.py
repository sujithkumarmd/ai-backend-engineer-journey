from dotenv import load_dotenv
from openai import OpenAI

MODEL = "gpt-6-luna"

load_dotenv()
client = OpenAI()

first = client.responses.create(
    model=MODEL,
    input="My name is Sujith. Please remember it.",
)
print("Call 1 reply:", first.output_text)
print()

second = client.responses.create(
    model=MODEL,
    input="What is my name?",
)
print("Call 2 reply:", second.output_text)
print()

third = client.responses.create(
    model=MODEL,
    input="What is today's date? Answer in one short sentence.",
)
print("Call 3 reply:", third.output_text)
