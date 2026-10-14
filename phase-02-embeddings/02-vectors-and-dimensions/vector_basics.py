import sys

# Three vectors in 3 dimensions: (animal-ness, food-ness, size)
cat = [0.9, 0.1, 0.2]
dog = [0.8, 0.2, 0.4]
pizza = [0.1, 0.9, 0.3]

# 1) Dimension = how many numbers
print("Dimension of cat:", len(cat))

# 2) Each position (index) always means the same thing
print("cat's food-ness (index 1):", cat[1])

# 3) Order matters: same numbers, different order = a different vector
print("Same vector?", [0.9, 0.1, 0.2] == [0.1, 0.9, 0.2])

# 4) Element-wise difference: compare position by position
difference = [round(a - b, 2) for a, b in zip(cat, dog, strict=True)]
print("cat - dog, position by position:", difference)

# 5) Vectors of different dimensions can't be compared
try:
    [a - b for a, b in zip(cat, [0.5, 0.5], strict=True)]
except ValueError as error:
    print("3-D vs 2-D:", error)

# 6) What does one 1536-dimension embedding cost to store?
DIMENSIONS = 1536
fake_embedding = [0.001 * i for i in range(DIMENSIONS)]
python_list_bytes = sys.getsizeof(fake_embedding) + sum(sys.getsizeof(x) for x in fake_embedding)
print(f"\nOne {DIMENSIONS}-dim vector:")
print(f"   as a Python list    : {python_list_bytes:>7,} bytes")
print(f"   as raw 8-byte floats: {DIMENSIONS * 8:>7,} bytes")
print(f"   as raw 4-byte floats: {DIMENSIONS * 4:>7,} bytes")
for count in [1_000, 1_000_000]:
    print(f"   {count:>9,} vectors at 4 bytes each: {count * DIMENSIONS * 4 / 1_000_000:,.1f} MB")
