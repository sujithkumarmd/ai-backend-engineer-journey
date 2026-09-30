import tiktoken

encoding = tiktoken.get_encoding("o200k_base")

texts = [
    "Hello",
    " hello",
    "Hello, how are you?",
    "unbelievable",
    "Sujith",
    "2026-09-28",
    "வணக்கம்",
]

for text in texts:
    token_ids = encoding.encode(text)
    pieces = [encoding.decode([token_id]) for token_id in token_ids]
    print(f"{text!r:<22} {len(token_ids)} tokens  ids={token_ids}  pieces={pieces}")

print()
round_trip = encoding.decode(encoding.encode("Hello, how are you?"))
print("Round trip:", round_trip)

paragraph = "The quick brown fox jumps over the lazy dog. " * 20
print(f"Paragraph: {len(paragraph)} characters, {len(paragraph.split())} words, "
      f"{len(encoding.encode(paragraph))} tokens")
