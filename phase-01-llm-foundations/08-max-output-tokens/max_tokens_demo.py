from dotenv import load_dotenv
from openai import OpenAI

MODEL = "gpt-6-luna"
PROMPT = "Explain how a refrigerator works in about 150 words."

load_dotenv()
client = OpenAI(timeout=60, max_retries=2)


def reply_or_warning(response):
    if response.status == "completed":
        return response.output_text
    reason = response.incomplete_details.reason if response.incomplete_details else "unknown"
    return f"⚠️ INCOMPLETE ({reason}). Partial text: {response.output_text!r}"


def ask(max_tokens, effort):
    response = client.responses.create(
        model=MODEL,
        input=PROMPT,
        max_output_tokens=max_tokens,
        reasoning={"effort": effort},
    )
    usage = response.usage
    print(f"effort={effort:<6} max_output_tokens={max_tokens:<5} status={response.status:<10} "
          f"output_tokens={usage.output_tokens:<4} (reasoning {usage.output_tokens_details.reasoning_tokens})")
    print(f"    → {reply_or_warning(response)[:160]}\n")


ask(20, "none")
ask(400, "none")
ask(50, "medium")
ask(2000, "medium")
