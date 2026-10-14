import math
import random

# Raw scores ("logits") a model might give 4 candidate next words after "The cat sat on the"
SCORES = {"mat": 3.0, "floor": 2.0, "sofa": 1.0, "moon": 0.0}


def probabilities(scores, temperature):
    scaled = {word: score / temperature for word, score in scores.items()}
    exponentials = {word: math.exp(value) for word, value in scaled.items()}
    total = sum(exponentials.values())
    return {word: value / total for word, value in exponentials.items()}


def sample(scores, temperature):
    if temperature == 0:
        return max(scores, key=scores.get)
    probs = probabilities(scores, temperature)
    return random.choices(list(probs.keys()), weights=list(probs.values()))[0]


for temperature in [0.2, 1.0, 2.0]:
    probs = probabilities(SCORES, temperature)
    shown = ", ".join(f"{word} {p:.2f}" for word, p in probs.items())
    picks = [sample(SCORES, temperature) for _ in range(10)]
    print(f"T={temperature}: {shown}")
    print(f"       10 picks: {' '.join(picks)}")

print("T=0  : always picks", sample(SCORES, 0))
