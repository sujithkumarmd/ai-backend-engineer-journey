import tiktoken
from dotenv import load_dotenv
from openai import OpenAI

MODEL = "gpt-6-luna"
PROMPT = "Explain what a token is in one sentence."

encoding = tiktoken.get_encoding("o200k_base")
print("tiktoken count of prompt :", len(encoding.encode(PROMPT)))

load_dotenv()
client = OpenAI()
response = client.responses.create(model=MODEL, input=PROMPT)

usage = response.usage
print("Reply                    :", response.output_text)
print()
print("API input_tokens         :", usage.input_tokens)
print("API output_tokens        :", usage.output_tokens)
print("  of which reasoning     :", usage.output_tokens_details.reasoning_tokens)
print("API total_tokens         :", usage.total_tokens)
print("tiktoken count of reply  :", len(encoding.encode(response.output_text)))
