import random
from collections import Counter, defaultdict

TRAINING_TEXT = """
the cat sat on the mat .
the cat sat on the sofa .
the dog sat on the mat .
the dog ate the food .
the cat ate the fish .
"""

# 1. "Training": count which word follows which
follow_counts = defaultdict(Counter)
words = TRAINING_TEXT.split()
for current_word, next_word in zip(words, words[1:]):
    follow_counts[current_word][next_word] += 1


# 2. Turn counts into probabilities
def next_word_probabilities(word):
    counts = follow_counts[word]
    total = sum(counts.values())
    return {candidate: round(count / total, 2) for candidate, count in counts.items()}


# 3. Generate: predict one word, append it, repeat
def generate(start_word, max_words=10):
    output = [start_word]
    for _ in range(max_words):
        probabilities = next_word_probabilities(output[-1])
        if not probabilities:
            break
        candidates = list(probabilities.keys())
        weights = list(probabilities.values())
        next_word = random.choices(candidates, weights=weights)[0]
        output.append(next_word)
        if next_word == ".":
            break
    return " ".join(output)


print("After 'the' :", next_word_probabilities("the"))
print("After 'sat' :", next_word_probabilities("sat"))
print()

for _ in range(3):
    print("Generated   :", generate("the"))

print("Unknown word:", generate("pizza"))
