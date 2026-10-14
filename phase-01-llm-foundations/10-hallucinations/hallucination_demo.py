from dotenv import load_dotenv
from openai import OpenAI

MODEL = "gpt-6-luna"

load_dotenv()
client = OpenAI(timeout=60, max_retries=2)


def ask(instructions, question):
    response = client.responses.create(
        model=MODEL,
        instructions=instructions,
        input=question,
        reasoning={"effort": "none"},
    )
    return response.output_text.strip()


# Part 1 & 2: a question about a paper that does NOT exist
FAKE_PAPER_QUESTION = (
    "Summarize the main findings of the 2019 paper 'Quantum Basil Growth in "
    "Low-Orbit Greenhouses' by Dr. Anaya Rao, in 3 bullet points."
)

print("=== 1. No guardrails ===")
print(ask("You are a helpful assistant.", FAKE_PAPER_QUESTION))

print("\n=== 2. Permission to say 'I don't know' ===")
print(ask(
    "You are a careful assistant. Only state facts you are confident are true. "
    "If you are not sure something exists, say so plainly instead of guessing.",
    FAKE_PAPER_QUESTION,
))

# Part 3: grounding — answer only from a provided document, then verify the quote
POLICY = """Acme Cloud refund policy (v3, March 2026)
Monthly plans can be refunded within 14 days of payment.
Annual plans can be refunded within 30 days of payment, minus one month of usage.
Refunds are paid back to the original payment method within 5 business days."""

GROUNDED_INSTRUCTIONS = (
    "Answer using ONLY the document inside <document> tags. "
    "If the answer is not in the document, reply exactly: Not in the document. "
    "Otherwise answer in one sentence, then on a new line write QUOTE: followed by "
    "the exact sentence from the document that supports your answer."
)


def check_quote(answer, document):
    if "QUOTE:" not in answer:
        return "no quote given"
    quote = answer.split("QUOTE:", 1)[1].strip().strip('"')
    if quote in document:
        return "✅ quote found word-for-word in the document"
    return "❌ quote NOT in the document (possible hallucination)"


for question in [
    "How long do I have to request a refund on a monthly plan?",
    "Can I get a refund on the Enterprise plan?",
]:
    answer = ask(GROUNDED_INSTRUCTIONS, f"<document>\n{POLICY}\n</document>\n\nQuestion: {question}")
    print(f"\n=== 3. Grounded: {question} ===")
    print(answer)
    print("   check:", check_quote(answer, POLICY))
