from dotenv import load_dotenv
from openai import OpenAI

from cost_calculator import calculate_cost

MODEL = "gpt-6-luna"
QUESTION = "Explain what an API is to a 10-year-old, in 3 sentences."

load_dotenv()
client = OpenAI(timeout=60, max_retries=2)

for effort in ["none", "medium"]:
    response = client.responses.create(
        model=MODEL,
        input=QUESTION,
        reasoning={"effort": effort},
    )
    usage = response.usage
    cached = usage.input_tokens_details.cached_tokens
    reasoning = usage.output_tokens_details.reasoning_tokens
    cost = calculate_cost(MODEL, usage.input_tokens, usage.output_tokens, cached)

    print(f"effort={effort}")
    print(f"   input tokens : {usage.input_tokens} (cached: {cached})")
    print(f"   output tokens: {usage.output_tokens} (reasoning: {reasoning}, visible: {usage.output_tokens - reasoning})")
    print(f"   cost         : ${cost:.6f}  →  ${cost * 1_000_000:,.2f} per million calls like this\n")
