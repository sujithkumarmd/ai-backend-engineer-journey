from dotenv import load_dotenv
from openai import OpenAI

MODEL = "gpt-6-luna"

load_dotenv()


client = OpenAI(timeout=60, max_retries=3)
response = client.responses.create(
    model=MODEL,
    input=[
            {'role': "user", "content": "Name a planet."}
        ]
    )



print("id          :", response.id)
print("model       :", response.model)
print("status      :", response.status)
print("output items:", [item.type for item in response.output])
print("reply       :", response.output_text)
print("usage       :", response.usage.input_tokens, "in /", response.usage.output_tokens, "out")
