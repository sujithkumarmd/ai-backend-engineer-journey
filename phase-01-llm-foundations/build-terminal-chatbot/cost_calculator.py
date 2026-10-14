# $ per 1M tokens, Standard tier. Checked on OpenAI's pricing page, 10 Oct 2026.
PRICES = {
    "gpt-6-luna": {"input": 0.10, "cached_input": 0.01, "output": 0.50},
    "gpt-6-sol": {"input": 2.00, "cached_input": 0.20, "output": 10.00},
    "gpt-6-astra": {"input": 10.00, "cached_input": 1.00, "output": 50.00},
}
LONG_CONTEXT_THRESHOLD = 272_000   # input tokens; above this the whole request costs more


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


if __name__ == "__main__":
    print("1) Same request (1,000 in + 500 out) on three models")
    for model in PRICES:
        print(f"   {model:<12} ${calculate_cost(model, 1_000, 500):.6f}")

    print("\n2) The 10-turn chat from Concept 06 (4,100 in + 600 out) on gpt-6-luna")
    chat_cost = calculate_cost("gpt-6-luna", 4_100, 600)
    print(f"   one chat          ${chat_cost:.6f}")
    print(f"   10,000 chats/day  ${chat_cost * 10_000:.2f} per day, ${chat_cost * 10_000 * 30:.2f} per month")

    print("\n3) Long-context rule on gpt-6-luna (1,000 output tokens)")
    for input_tokens in [272_000, 272_001]:
        print(f"   {input_tokens:,} input tokens → ${calculate_cost('gpt-6-luna', input_tokens, 1_000):.6f}")

    print("\n4) Cached input: 10,000 input tokens, 8,000 of them cached, 200 out (gpt-6-luna)")
    print(f"   no cache   ${calculate_cost('gpt-6-luna', 10_000, 200):.6f}")
    print(f"   with cache ${calculate_cost('gpt-6-luna', 10_000, 200, cached_tokens=8_000):.6f}")
