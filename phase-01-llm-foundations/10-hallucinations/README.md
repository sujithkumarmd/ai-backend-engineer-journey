<div align="center">

# 🤥 Concept 10 — Hallucinations

![Phase](https://img.shields.io/badge/Phase%201-LLM%20Foundations-blueviolet?style=flat-square)
![Concept](https://img.shields.io/badge/concept-10%20of%2012-blue?style=flat-square)
![Status](https://img.shields.io/badge/status-done-brightgreen?style=flat-square)

**A hallucination is fluent, confident output that is false or unsupported. You can't switch it off, but you can make it rarer and catch it.**

[⬅️ 09 · Prompt structure & few-shot](../09-prompt-structure-and-few-shot/) · [📂 Phase 1 index](../README.md) · [🗺️ Roadmap](../../README.md) · Next ➡️ [11 · Reasoning models](../11-reasoning-models/)

</div>

---

## 🎯 What you'll be able to do after this

- [x] Define hallucination and name its common types
- [x] Explain **why** LLMs hallucinate
- [x] Reduce hallucinations with permission to abstain, grounding, and quotes
- [x] Verify a model's claim with plain Python instead of trusting it

---

## 🧠 1. Intuition

Picture a student in an exam who **never leaves a question blank**. If they don't know, they write something that *sounds* right, confidently, in perfect sentences. Sometimes they're lucky; often they're wrong.

LLMs behave like that student:

- They're built to produce the **most plausible next text** (Concept 01), not to check facts.
- A blank answer scores zero on most tests, so **guessing is rewarded**.
- Their tone is equally confident whether they're right or wrong. **Confidence is not evidence.**

You already saw a tiny hallucination in Concept 01: your toy model wrote `the cat ate the dog ate the mat .`. Each step was plausible; the whole thing was false.

---

## ⚙️ 2. Technical Explanation

### Definition and types

A **hallucination** is model output that sounds fluent and confident but is **false, invented, or not supported** by the information it was given.

| Type | Example | Why it hurts a backend engineer |
|---|---|---|
| **Factual error** | Wrong date, wrong number, wrong person | Users trust and repeat it |
| **Fabricated source** | A citation, paper, or URL that doesn't exist | Looks authoritative, impossible to verify |
| **Fabricated code/API** | A library function or API parameter that doesn't exist | Your code breaks at runtime |
| **Unfaithful to context** | In RAG, the answer adds or changes facts from the provided document | The whole point of RAG is defeated *(Phase 7: "faithfulness")* |
| **Fake self-knowledge** | "I'll remember that for next time!" (Concept 01) | Promises the system can't keep |

### Why it happens

| Cause | Explanation |
|---|---|
| **Next-token prediction** | The model optimizes for *plausible*, not *true* (Concept 01) |
| **Knowledge gaps** | Rare facts, recent events after the knowledge cutoff (18 May 2026 for `gpt-6-luna`), private company data it never saw |
| **Guessing is rewarded** | OpenAI's 2025 research paper *"Why Language Models Hallucinate"* argues that standard training and evaluation **reward guessing over admitting uncertainty**, like a multiple-choice test where a blank scores zero but a guess might score a point |
| **The prompt assumes something false** | "Summarize the paper by Dr. X…" presumes the paper exists, nudging the model to play along |
| **High temperature** | More chances to pick unlikely (and wrong) tokens (Concept 07) |

### How to reduce it (defense in depth again)

| Technique | How | Where you'll go deeper |
|---|---|---|
| 🚪 **Permission to abstain** | Explicitly allow "I don't know" / "Not in the document" | This lesson |
| 📄 **Grounding** | Put the relevant facts **in the prompt** and say "answer only from this" | **Phase 3 (RAG)**, the main fix |
| 🔎 **Quotes / citations** | Make the model point to the exact supporting sentence | This lesson; Phase 3 citations |
| ✅ **Programmatic verification** | Check claims with code: quote exists? JSON valid? ID exists in the database? | This lesson; Phase 8 validation |
| 🧊 **Low temperature** | For factual tasks | Concept 07 |
| 🧰 **Tools** | Let the model look things up instead of recalling them | Phase 8 |
| 📏 **Evaluation** | Measure hallucination rates on test sets | Phase 7 (faithfulness, LLM-as-judge) |

> [!IMPORTANT]
> **Abstention** (the model saying "I don't know") is a *feature*, not a failure. A support bot that says "I'm not sure, let me connect you to a human" is far better than one that invents a refund policy.

---

## 🔢 3. Tiny Example

**The question:** *"Summarize the 2019 paper 'Quantum Basil Growth in Low-Orbit Greenhouses' by Dr. Anaya Rao."* **This paper doesn't exist; we made it up.**

| Prompt | Likely behavior |
|---|---|
| "You are a helpful assistant." | ⚠️ May write three convincing bullet points about basil yields in orbit |
| "+ If you are not sure something exists, say so." | ✅ "I couldn't find/verify this paper…" |

**Grounding with a verifiable quote:** the document says *"Monthly plans can be refunded within 14 days of payment."*

| Model's answer | `quote in document`? | Verdict |
|---|:-:|---|
| `QUOTE: Monthly plans can be refunded within 14 days of payment.` | ✅ True | Supported |
| `QUOTE: Monthly plans are refundable for two weeks.` | ❌ False | Paraphrased or invented: flag it |
| `Not in the document.` | n/a | Honest abstention |

*(These three checks are real outputs of the script's `check_quote()` function, tested offline.)*

---

## 💻 4. Code — [`hallucination_demo.py`](hallucination_demo.py)

4 tiny calls, a fraction of a cent.

### Piece 1: a small helper

```python
def ask(instructions, question):
    response = client.responses.create(
        model=MODEL,
        instructions=instructions,
        input=question,
        reasoning={"effort": "none"},
    )
    return response.output_text.strip()
```

`reasoning={"effort": "none"}` = answer directly, without thinking first: the setting where bluffing is most likely, which is good for a demo.

### Piece 2: a fake paper, with and without permission to abstain

```python
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
```

| Line | What it does |
|---|---|
| `( "..." "..." )` | Two strings side by side inside parentheses are **joined automatically**: a neat way to split a long string over lines |
| The question itself | Presumes the paper exists, the classic hallucination trap |
| Version 2's instructions | Gives explicit **permission to abstain** |

### Piece 3: grounding + a programmatic check

```python
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
```

| Line | What it does |
|---|---|
| `POLICY` | A tiny "knowledge base": the only facts the model may use. **This is RAG in miniature** (Phase 3) |
| `GROUNDED_INSTRUCTIONS` | Three rules: only use the document, an exact abstain phrase, and a supporting quote |
| `answer.split("QUOTE:", 1)[1]` | Split at the first `QUOTE:` only (`1` = max one split) and take the part after it |
| `.strip().strip('"')` | Remove surrounding spaces, then surrounding double quotes if the model added them |
| `quote in document` | Plain substring check: **Python verifies the model's claim** instead of trusting it |

### Piece 4: one answerable and one unanswerable question

```python
for question in [
    "How long do I have to request a refund on a monthly plan?",
    "Can I get a refund on the Enterprise plan?",
]:
    answer = ask(GROUNDED_INSTRUCTIONS, f"<document>\n{POLICY}\n</document>\n\nQuestion: {question}")
    print(f"\n=== 3. Grounded: {question} ===")
    print(answer)
    print("   check:", check_quote(answer, POLICY))
```

The document never mentions an "Enterprise plan", so the honest answer is exactly `Not in the document.`

```bash
python phase-01-llm-foundations/10-hallucinations/hallucination_demo.py
```

**What to look for:**

| Section | Good sign | Bad sign |
|---|---|---|
| 1. No guardrails | It says it can't find the paper | Three confident bullet points about a paper that doesn't exist |
| 2. Permission to abstain | Clearly says it can't verify the paper | Still invents findings |
| 3a. Monthly refund | "14 days" + ✅ quote check | ❌ quote check (paraphrased) |
| 3b. Enterprise plan | `Not in the document.` | An invented Enterprise policy |

> [!NOTE]
> Modern models are increasingly good at spotting obviously fake things, so section 1 may **not** hallucinate for you. That's fine; the lesson is that you can't *rely* on that. Try a subtler fake (a real-sounding author and a plausible title in your own field) and see.

---

## 🎤 5. Interview Answer

> *"A hallucination is fluent, confident output that's false or unsupported by the provided context. It comes from next-token prediction optimizing for plausibility, knowledge gaps, and training and evaluation that reward guessing over abstaining. I reduce it in layers: ground answers in retrieved context, explicitly allow 'I don't know', require citations or quotes, keep temperature low for factual tasks, and verify outputs in code (quotes exist in the source, IDs exist in the database), then measure faithfulness on an evaluation set rather than trusting the model's confidence."*

---

## 📌 Cheat Sheet

| Goal | Technique |
|---|---|
| Allow honesty | "If you're not sure, say you don't know." |
| Ground in facts | "Answer ONLY from `<document>…</document>`." |
| Exact abstain phrase | "If it's not in the document, reply exactly: Not in the document." |
| Make it checkable | "Quote the exact supporting sentence after `QUOTE:`." |
| Verify in code | `quote in document` |
| Factual tasks | Low temperature (Concept 07) |
| Fresh/private facts | RAG (Phase 3) or tools (Phase 8), never memory |

---

## ⚠️ Common Mistakes

| Mistake | Consequence | Fix |
|---|---|---|
| Trusting confident tone | Shipping false answers | Verify; confidence ≠ correctness |
| Questions that presume false facts | The model plays along | Ask neutrally; allow abstention |
| Asking for citations without a source | Fabricated references | Provide the sources; verify every citation |
| "Answer only from the document" without an abstain path | The model invents when the doc lacks the answer | Give an exact fallback phrase |
| Using AI-suggested library functions blindly | Code calls functions that don't exist | Check the docs or run the code |
| Treating "no hallucination in my 3 tests" as proof | Surprises in production | Measure on many cases *(Phase 7)* |

---

## 📖 Glossary

| Term | Plain meaning |
|---|---|
| **Hallucination** | Fluent, confident output that's false or unsupported |
| **Grounding** | Giving the model the facts it should use, in the prompt |
| **Abstention** | The model declining to answer ("I don't know") |
| **Faithfulness** | Whether an answer sticks to the provided context *(Phase 7)* |
| **Citation / quote** | Pointer to the exact source text supporting a claim |
| **Programmatic verification** | Checking model output with code instead of trusting it |
| **Knowledge cutoff** | Date the training data ends; later facts are unknown |
| **Long-tail facts** | Rare facts that appeared little in training data; most hallucination-prone |
| **Implicit string concatenation** | `("a" "b")` → `"ab"`: adjacent strings join automatically |

---

<div align="center">

**Status:** ✅ DONE · completed Thu 01 Oct 2026

[⬅️ 09 · Prompt structure & few-shot](../09-prompt-structure-and-few-shot/) · [📂 Phase 1 index](../README.md) · [🗺️ Roadmap](../../README.md)

</div>

<sub>Sources: [OpenAI — Why language models hallucinate](https://openai.com/index/why-language-models-hallucinate/) · [Kalai et al., 2025, arXiv:2509.04664](https://arxiv.org/abs/2509.04664) · [OpenAI — GPT-6 Luna](https://developers.openai.com/api/docs/models/gpt-6-luna) (knowledge cutoff)</sub>
