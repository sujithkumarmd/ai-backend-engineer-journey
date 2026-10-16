import math

import numpy as np

cat = [0.9, 0.1, 0.2]
dog = [0.8, 0.2, 0.4]
pizza = [0.1, 0.9, 0.3]


# 1) From scratch, plain Python
def dot_product(a, b):
    return sum(x * y for x, y in zip(a, b, strict=True))


def norm(a):
    return math.sqrt(sum(x * x for x in a))


print("From scratch:")
print(f"   dot(cat, dog)   = {dot_product(cat, dog):.2f}")
print(f"   dot(cat, pizza) = {dot_product(cat, pizza):.2f}")
print(f"   norm([3, 4])    = {norm([3, 4]):.2f}")
print(f"   norm(cat)       = {norm(cat):.3f}")
print(f"   sqrt(dot(cat, cat)) = {math.sqrt(dot_product(cat, cat)):.3f}   (same as norm)")

# 2) The same with NumPy
cat_np, dog_np = np.array(cat), np.array(dog)
print("\nNumPy:")
print(f"   np.dot(cat, dog)       = {np.dot(cat_np, dog_np):.2f}")
print(f"   cat @ dog              = {cat_np @ dog_np:.2f}")
print(f"   np.linalg.norm(cat)    = {np.linalg.norm(cat_np):.3f}")

# 3) One query against every row at once: matrix @ query
items = ["cat", "dog", "pizza"]
matrix = np.array([cat, dog, pizza])
query = np.array([0.85, 0.15, 0.3])
scores = matrix @ query
print("\nmatrix @ query (one dot product per row):")
for item, score in zip(items, scores):
    print(f"   {item:<6} {score:.3f}")
print("   best match:", items[int(np.argmax(scores))])

# 4) The length problem: same direction, double the length
big_dog = np.array(dog) * 2
print("\nThe length problem:")
print(f"   dog     = {np.array(dog)}  norm {np.linalg.norm(dog):.3f}  dot with cat {cat_np @ np.array(dog):.2f}")
print(f"   big_dog = {big_dog}  norm {np.linalg.norm(big_dog):.3f}  dot with cat {cat_np @ big_dog:.2f}")
