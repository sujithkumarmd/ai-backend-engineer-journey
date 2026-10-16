import math

import numpy as np


# 1) From scratch, built on Concept 04's two functions
def dot_product(a, b):
    return sum(x * y for x, y in zip(a, b, strict=True))


def norm(a):
    return math.sqrt(sum(x * x for x in a))


def cosine_similarity(a, b):
    return dot_product(a, b) / (norm(a) * norm(b))


# 2) Angles you can picture, in 2-D
east = [1, 0]
print("Direction check (2-D):")
for name, other in [("same way     ", [2, 0]), ("45° apart    ", [1, 1]),
                    ("right angle  ", [0, 1]), ("opposite     ", [-1, 0])]:
    print(f"   {name} {other!s:<8} cosine = {cosine_similarity(east, other):6.3f}")

# 3) The length problem from Concept 04: fixed
cat = [0.9, 0.1, 0.2]
dog = [0.8, 0.2, 0.4]
big_dog = [x * 2 for x in dog]
print("\nThe length problem, fixed:")
print(f"   dot(cat, dog)     = {dot_product(cat, dog):.3f}   cosine = {cosine_similarity(cat, dog):.3f}")
print(f"   dot(cat, big_dog) = {dot_product(cat, big_dog):.3f}   cosine = {cosine_similarity(cat, big_dog):.3f}")


# 4) NumPy: one query against every row
def cosine_scores(matrix, query):
    return (matrix @ query) / (np.linalg.norm(matrix, axis=1) * np.linalg.norm(query))


items = ["cat", "dog", "pizza", "big_dog"]
matrix = np.array([cat, dog, [0.1, 0.9, 0.3], big_dog])
query = np.array([0.85, 0.15, 0.3])

print("\nQuery vs every row:")
print(f"   {'item':<8} {'dot':>6} {'cosine':>7}")
for item, dot, cosine in zip(items, matrix @ query, cosine_scores(matrix, query)):
    print(f"   {item:<8} {dot:6.3f} {cosine:7.3f}")
