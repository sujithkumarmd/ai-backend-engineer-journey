import openai
from dotenv import load_dotenv
from openai import OpenAI

MODEL = "gpt-6-luna"
PROMPT = "Invent a name for a coffee shop. Reply with the name only."

load_dotenv()
client = OpenAI(timeout=60, max_retries=2)


def three_names(temperature, effort):
    names = []
    for _ in range(3):
        response = client.responses.create(
            model=MODEL,
            input=PROMPT,
            temperature=temperature,
            reasoning={"effort": effort},
        )
        names.append(response.output_text.strip())
    return names


for effort in ["none", "medium"]:
    for temperature in [0.0, 1.5]:
        try:
            names = three_names(temperature, effort)
            print(f"effort={effort:<6} temperature={temperature}: {names}")
        except openai.BadRequestError as error:
            print(f"effort={effort:<6} temperature={temperature}: ❌ 400 {error.message[:120]}")
