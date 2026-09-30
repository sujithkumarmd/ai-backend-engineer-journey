import tiktoken

CONTEXT_WINDOW = 70          # a tiny pretend model, so we can overflow it easily
RESERVED_FOR_REPLY = 20      # tokens kept free for the model's answer

encoding = tiktoken.get_encoding("o200k_base")


def count_tokens(messages):
    return sum(len(encoding.encode(message)) for message in messages)


def trim_to_fit(messages):
    budget = CONTEXT_WINDOW - RESERVED_FOR_REPLY
    trimmed = list(messages)
    while trimmed and count_tokens(trimmed) > budget:
        dropped = trimmed.pop(0)
        print(f"   ✂️  dropped oldest: {dropped!r}")
    return trimmed


conversation = []
turns = [
    "Hi, my name is Sujith.",
    "I work as a backend engineer and I mostly write Python.",
    "Right now I am learning how to build AI features.",
    "Today I am studying context windows and tokens.",
    "What is my name?",
]

for turn in turns:
    conversation.append(turn)
    input_budget = CONTEXT_WINDOW - RESERVED_FOR_REPLY
    print(f"Added turn → {count_tokens(conversation)} / {input_budget} input tokens")
    conversation = trim_to_fit(conversation)

print("\nWhat the model would actually see:")
for message in conversation:
    print("  •", message)
