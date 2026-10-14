<div align="center">

# 💵 Concept 12 — Cost Calculation

![Phase](https://img.shields.io/badge/Phase%201-LLM%20Foundations-blueviolet?style=flat-square)
![Concept](https://img.shields.io/badge/concept-12%20of%2012-blue?style=flat-square)
![Status](https://img.shields.io/badge/status-done-brightgreen?style=flat-square)

**Every call has a price: input tokens × input price + output tokens × output price. Know the formula, and you can predict a bill before you ship.**

[⬅️ 11 · Reasoning models](../11-reasoning-models/) · [📂 Phase 1 index](../README.md) · [🗺️ Roadmap](../../README.md) · Next ➡️ [🔨 Build: terminal chatbot](../build-terminal-chatbot/)

</div>

---

## 🎯 What you'll be able to do after this

- [x] Calculate the cost of any call from its `usage`
- [x] Explain why output tokens cost more than input tokens
- [x] Account for cached input, reasoning tokens and the long-context rule
- [x] Project a monthly bill from per-call numbers
- [x] Compare models and processing tiers by price

---

## 🧠 1. Intuition

A taxi has one meter. An LLM call has **two**:

| Meter | Counts | Price |
|---|---|---|
| 📥 **Input meter** | Every token you **send**: instructions, chat history, documents, your question | Cheaper |
| 📤 **Output meter** | Every token the model **writes**: hidden reasoning + the visible reply | **More expensive** (5× for `gpt-6-luna`) |

The fare is simply the two meters added together. Everything you learned in Phase 1 moves one of these meters:

| Concept | Which meter it moves |
|---|---|
| 02 Tokens | Both: tokens are the unit |
| 03 Context window / 06 Chat history | 📥 Input grows every turn |
| 08 Max output tokens | 📤 Caps the output meter |
| 09 Few-shot examples | 📥 Input, on every call |
| 11 Reasoning effort | 📤 Output (hidden reasoning tokens) |

---

## ⚙️ 2. Technical Explanation

### The formula

Prices are quoted **per 1 million tokens** ("per 1M"), so divide by 1,000,000 to get the price of one token:

```text
cost = input_tokens  × input_price  ÷ 1,000,000
     + output_tokens × output_price ÷ 1,000,000
```

The token counts come from `response.usage` (Concept 02), the **source of truth** for billing.

### Current prices (Standard tier, checked 10 Oct 2026)

| Model | Input / 1M | Cached input / 1M | Output / 1M | Output ÷ input |
|---|:-:|:-:|:-:|:-:|
| `gpt-6-luna` ⭐ | $0.10 | $0.01 | $0.50 | 5× |
| `gpt-6-sol` | $2.00 | $0.20 | $10.00 | 5× |
| `gpt-6-astra` | $10.00 | $1.00 | $50.00 | 5× |

`gpt-6-astra` costs **100×** as much as `gpt-6-luna` for the same tokens ($10.00 ÷ $0.10 = 100).

### Why output costs more

Input tokens are all read **in one pass**. Output tokens are generated **one at a time** (Concept 01's loop), and each new token needs another pass through the model. More computing work per token → higher price.

### Four details that change the bill

| Detail | Rule | Effect |
|---|---|---|
| **Reasoning tokens** | Already **inside** `output_tokens` | Billed at the output price, even though you never see them (Concept 11) |
| **Cached input** | Part of `input_tokens`, reported as `usage.input_tokens_details.cached_tokens` | Billed at the **cached** price: 10% of normal input for these models |
| **Long-context rule** | Prompts with **more than 272,000 input tokens**: **2× input** and cache rates, **1.5× output**, for the **whole** request | Crossing the line by one token almost doubles the bill |
| **Processing tier** | Batch and Flex: **50%** of Standard. Fast mode: **2×** Standard | Trade speed for price |

**Cached input** = when many requests start with the same long prefix (for example the same instructions), the provider can reuse work it already did and charge less for those tokens. This is called **prompt caching** and is a Phase 10 topic; short prompts like ours normally show `cached: 0`. (Storing a prefix in the cache has its own "cache write" price, also covered there.)

**Tiers in one line each:**

| Tier | Meaning |
|---|---|
| **Standard** | Normal, immediate processing |
| **Batch** | Submit many requests together and collect results later, at half price |
| **Flex** | Slower, lower-priority processing at half price |
| **Fast** | Faster processing at double price (renamed from "Priority processing" on 30 Jul 2026) |

### From one call to a monthly bill

```text
monthly cost = cost per call × calls per day × 30
```

Tiny per-call numbers become real money at scale, so you calculate **before** launching, not after the invoice.

---

## 🔢 3. Tiny Example

**One call: 1,000 input tokens + 500 output tokens on `gpt-6-luna`**

| Part | Math | Cost |
|---|---|---|
| Input | 1,000 × $0.10 ÷ 1,000,000 | $0.000100 |
| Output | 500 × $0.50 ÷ 1,000,000 | $0.000250 |
| **Total** | | **$0.000350** |

Notice the output is **half** the tokens but **71%** of the cost ($0.00025 ÷ $0.00035).

**Same call on three models** (real output of `cost_calculator.py`):

| Model | Cost | vs luna |
|---|:-:|:-:|
| `gpt-6-luna` | $0.000350 | 1× |
| `gpt-6-sol` | $0.007000 | 20× |
| `gpt-6-astra` | $0.035000 | 100× |

**The 10-turn chat from Concept 06** (4,100 input + 600 output tokens):

| | Math | Cost |
|---|---|---|
| One chat | 4,100 × $0.10/1M + 600 × $0.50/1M = $0.00041 + $0.00030 | **$0.00071** |
| 10,000 chats/day | $0.00071 × 10,000 | **$7.10 / day** |
| Per month | $7.10 × 30 | **$213 / month** |

**The long-context cliff:**

| Input tokens | Cost (with 1,000 output tokens) |
|---:|:-:|
| 272,000 | $0.027700 |
| 272,001 | **$0.055150** |

One extra token → **1.99×** the price ($0.05515 ÷ $0.0277), because the higher rates apply to the *whole* request.

**Caching:** 10,000 input tokens (8,000 cached) + 200 output: **$0.00038** instead of $0.00110, a **65% saving** (1 − 0.00038 ÷ 0.00110).

---

## 💻 4. Code

### Script 1 — A cost calculator from scratch: [`cost_calculator.py`](cost_calculator.py)

No API, no cost. You'll **reuse this file in the chatbot build**.

**Piece 1: the price table**

```python
# $ per 1M tokens, Standard tier. Checked on OpenAI's pricing page, 10 Oct 2026.
PRICES = {
    "gpt-6-luna": {"input": 0.10, "cached_input": 0.01, "output": 0.50},
    "gpt-6-sol": {"input": 2.00, "cached_input": 0.20, "output": 10.00},
    "gpt-6-astra": {"input": 10.00, "cached_input": 1.00, "output": 50.00},
}
LONG_CONTEXT_THRESHOLD = 272_000   # input tokens; above this the whole request costs more
```

| Line | What it does |
|---|---|
| `PRICES = {...}` | A dict of dicts: model name → its three prices. One place to update when prices change |
| The date comment | Prices change often; always record **when** you checked |
| `272_000` | Same as 272000; underscores are for readability |

**Piece 2: the function**

```python
def calculate_cost(model, input_tokens, output_tokens, cached_tokens=0):
    price = PRICES[model]

    if input_tokens > LONG_CONTEXT_THRESHOLD:
        input_multiplier, output_multiplier = 2.0, 1.5
    else:
        input_multiplier, output_multiplier = 1.0, 1.0

    uncached_tokens = input_tokens - cached_tokens
    input_cost = uncached_tokens * price["input"] / 1_000_000 * input_multiplier
    cached_cost = cached_tokens * price["cached_input"] / 1_000_000 * input_multiplier
    output_cost = output_tokens * price["output"] / 1_000_000 * output_multiplier
    return input_cost + cached_cost + output_cost
```

| Line | What it does |
|---|---|
| `cached_tokens=0` | Optional argument: if you don't pass it, it's 0 |
| `price = PRICES[model]` | Look up this model's prices. An unknown model raises `KeyError`, which is good: better to crash than to bill at a guessed price |
| `if input_tokens > LONG_CONTEXT_THRESHOLD` | The long-context rule: both multipliers change together |
| `a, b = 2.0, 1.5` | **Tuple unpacking**: assign two variables in one line |
| `uncached_tokens = input_tokens - cached_tokens` | `input_tokens` **includes** the cached ones, so subtract to avoid charging them twice |
| `/ 1_000_000` | Convert "per 1M tokens" into "per token" |
| `return ... + ... + ...` | Three parts: normal input + cached input + output (reasoning is already inside `output_tokens`) |

**Piece 3: try it, only when run directly**

```python
if __name__ == "__main__":
    print("1) Same request (1,000 in + 500 out) on three models")
    for model in PRICES:
        print(f"   {model:<12} ${calculate_cost(model, 1_000, 500):.6f}")
    ...
```

| Line | What it does |
|---|---|
| `if __name__ == "__main__":` | Python sets `__name__` to `"__main__"` only when a file is **run directly**. When another file **imports** it, this block is skipped. So the file works both as a script (prints the demo) and as a reusable module (just provides the function) |
| `for model in PRICES` | Looping over a dict gives its keys (the model names) |
| `:.6f` | Six decimal places, because per-call costs are tiny |

```bash
python phase-01-llm-foundations/12-cost-calculation/cost_calculator.py
```

Real output:

```text
1) Same request (1,000 in + 500 out) on three models
   gpt-6-luna   $0.000350
   gpt-6-sol    $0.007000
   gpt-6-astra  $0.035000

2) The 10-turn chat from Concept 06 (4,100 in + 600 out) on gpt-6-luna
   one chat          $0.000710
   10,000 chats/day  $7.10 per day, $213.00 per month

3) Long-context rule on gpt-6-luna (1,000 output tokens)
   272,000 input tokens → $0.027700
   272,001 input tokens → $0.055150

4) Cached input: 10,000 input tokens, 8,000 of them cached, 200 out (gpt-6-luna)
   no cache   $0.001100
   with cache $0.000380
```

### Script 2 — Price a real call: [`real_call_cost.py`](real_call_cost.py)

2 tiny calls.

```python
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
```

| Line | What it does |
|---|---|
| `from cost_calculator import calculate_cost` | Imports the function from Script 1. It works because Python looks for modules in the **folder of the script you run**. The `__main__` demo block does **not** run |
| `usage.input_tokens_details.cached_tokens` | How many input tokens were served from cache (expect 0 here) |
| `usage.output_tokens - reasoning` | Visible reply tokens = all output − hidden reasoning |
| `cost * 1_000_000` | A scale-up that makes tiny numbers readable: "what would a million of these cost?" |
| `:,.2f` | Thousands separators and 2 decimals, e.g. `1,234.50` |

```bash
python phase-01-llm-foundations/12-cost-calculation/real_call_cost.py
```

**✅ Verified result (real run, 11 Oct 2026):**

```text
effort=none
   input tokens : 23 (cached: 0)
   output tokens: 46 (reasoning: 0, visible: 46)
   cost         : $0.000025  →  $25.30 per million calls like this

effort=medium
   input tokens : 23 (cached: 0)
   output tokens: 78 (reasoning: 27, visible: 51)
   cost         : $0.000041  →  $41.30 per million calls like this
```

| Check | Math |
|---|---|
| `none` | 23 × $0.10/1M + 46 × $0.50/1M = $0.0000023 + $0.000023 = **$0.0000253** |
| `medium` | 23 × $0.10/1M + 78 × $0.50/1M = $0.0000023 + $0.000039 = **$0.0000413** |
| Price of thinking | 27 reasoning tokens × $0.50/1M = $0.0000135, making the call **1.63×** as expensive ($41.30 ÷ $25.30) |
| Output's share | At `none`, output is 91% of the cost ($0.000023 ÷ $0.0000253) |

---

## 🎤 5. Interview Answer

> *"LLM cost is input tokens times the input price plus output tokens times the output price, with prices quoted per million tokens and output typically several times more expensive because it's generated token by token. I compute it from the API's usage data rather than estimates, remembering that reasoning tokens are billed as output, cached input is discounted, and some models charge more above a long-context threshold. Then I project per-call cost to monthly volume and pull the main levers: a cheaper model, lower reasoning effort, shorter prompts and history, output caps, prompt caching, and batch processing for non-urgent work."*

---

## 📌 Cheat Sheet

| Task | Code / formula |
|---|---|
| Cost of a call | `in × in_price/1M + out × out_price/1M` |
| Token counts | `response.usage.input_tokens`, `.output_tokens` |
| Cached input tokens | `response.usage.input_tokens_details.cached_tokens` |
| Reasoning tokens | `response.usage.output_tokens_details.reasoning_tokens` (inside `output_tokens`) |
| `gpt-6-luna` | $0.10 in · $0.01 cached · $0.50 out, per 1M |
| Long context | > 272,000 input tokens → 2× input, 1.5× output, whole request |
| Batch / Flex / Fast | 50% / 50% / 200% of Standard |
| Monthly | `cost_per_call × calls_per_day × 30` |
| Reusable module | `if __name__ == "__main__":` around demo code |

### 💡 The cost levers (cheapest first to try)

| Lever | From |
|---|---|
| Use the cheapest model that passes your tests | Phase 0 · 07 |
| Lower reasoning effort | Concept 11 |
| Shorter prompts, fewer examples | Concept 09 |
| Trim or summarize chat history | Concepts 03, 06 |
| Cap output and ask for concise answers | Concept 08 |
| Send only relevant context (RAG) | Phase 3 |
| Prompt caching, batch processing, model routing | Phase 10 |

---

## ⚠️ Common Mistakes

| Mistake | Consequence | Fix |
|---|---|---|
| Forgetting the ÷ 1,000,000 | Costs a million times too high | Prices are **per 1M** tokens |
| Pricing output at the input rate | Underestimates by up to 5× | Two meters, two prices |
| Ignoring reasoning tokens | Real bill far above the estimate | Use `usage.output_tokens` (includes them) |
| Estimating from word counts | Off by 25% or more | Use tokens from `usage` |
| Hardcoding prices with no date | Silent wrong costs after a price change | One table, with the date checked |
| Pricing one call, not the conversation | Misses history resend growth | Sum over all turns (Concept 06) |
| Sitting just above 272K input | ~2× the bill | Trim below the threshold |
| Using floats for real invoices | Tiny rounding errors add up | For billing systems use `decimal.Decimal`; floats are fine for estimates |

---

## 📖 Glossary

| Term | Plain meaning |
|---|---|
| **Per 1M tokens** | Price for one million tokens; divide by 1,000,000 for one token |
| **Input / output price** | Rate for tokens you send / tokens the model generates |
| **Cached input** | Input tokens the provider recognized from an earlier identical prefix; billed cheaper |
| **Prompt caching** | The feature that produces cached input *(Phase 10)* |
| **Long-context pricing** | Higher rates once input exceeds a threshold |
| **Standard / Batch / Flex / Fast** | Processing tiers trading speed for price |
| **Usage** | The token counts returned with each response |
| **Unit economics** | What one unit (one call, one chat, one user) costs you |
| **`__name__ == "__main__"`** | True only when a file is run directly, not imported |
| **Module** | A Python file whose functions other files can import |
| **Tuple unpacking** | `a, b = 1, 2`: assign several variables at once |

---

<div align="center">

**Status:** ✅ DONE · completed Sun 11 Oct 2026 · verified: medium effort cost 1.63× none for the same question

[⬅️ 11 · Reasoning models](../11-reasoning-models/) · [📂 Phase 1 index](../README.md) · [🗺️ Roadmap](../../README.md)

</div>

<sub>Sources: [OpenAI — Pricing](https://developers.openai.com/api/docs/pricing) and [OpenAI — GPT-6 Luna](https://developers.openai.com/api/docs/models/gpt-6-luna), both checked 10 Oct 2026 · `openai` 3.19.2 SDK (`usage` fields) · all example numbers produced by `cost_calculator.py`</sub>
