import time

from dotenv import load_dotenv
from openai import OpenAI

MODEL = "gpt-6-luna"
INPUT_PRICE = 0.10 / 1_000_000    # $ per input token
OUTPUT_PRICE = 0.50 / 1_000_000   # $ per output token (reasoning tokens included)

TEXT = "strawberry raspberry cranberry blueberry"
QUESTION = f"How many times does the letter 'r' appear in: {TEXT}? Reply with just the number."
CORRECT = TEXT.count("r")          # ground truth computed by Python, not by the model

load_dotenv()
client = OpenAI(timeout=120, max_retries=2)

print(f"Correct answer (counted by Python): {CORRECT}\n")

# Part 1: same question, four reasoning efforts
for effort in ["none", "low", "medium", "high"]:
    start = time.perf_counter()
    response = client.responses.create(
        model=MODEL,
        input=QUESTION,
        reasoning={"effort": effort},
    )
    seconds = time.perf_counter() - start

    usage = response.usage
    cost = usage.input_tokens * INPUT_PRICE + usage.output_tokens * OUTPUT_PRICE
    answer = response.output_text.strip()
    verdict = "✅" if answer == str(CORRECT) else "❌"

    print(f"effort={effort:<6} {verdict} answer={answer!r:<6} "
          f"reasoning_tokens={usage.output_tokens_details.reasoning_tokens:<5} "
          f"time={seconds:5.1f}s  cost=${cost:.6f}")

# Part 2: peek at a summary of the hidden reasoning
response = client.responses.create(
    model=MODEL,
    input=QUESTION,
    reasoning={"effort": "medium", "summary": "auto"},
)
print("\nReasoning summary (medium effort):")
for item in response.output:
    if item.type == "reasoning":
        for part in item.summary:
            print("  •", part.text)
print("Final answer:", response.output_text)
