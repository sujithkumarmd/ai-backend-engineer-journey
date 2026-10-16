import numpy as np

# 1) A vector as a NumPy array
cat = np.array([0.9, 0.1, 0.2])
dog = np.array([0.8, 0.2, 0.4])
print("cat:", cat)
print("shape:", cat.shape, "| dtype:", cat.dtype, "| bytes:", cat.nbytes)

# 2) Element-wise math without a loop
print("\ncat - dog:", cat - dog)
print("cat * 2  :", cat * 2)
print("cat * dog:", cat * dog)

# 3) Many vectors stacked into one 2-D array (a matrix): one row per item
items = ["cat", "dog", "pizza"]
matrix = np.array([
    [0.9, 0.1, 0.2],
    [0.8, 0.2, 0.4],
    [0.1, 0.9, 0.3],
])
print("\nmatrix shape:", matrix.shape, "→", matrix.shape[0], "vectors of", matrix.shape[1], "dimensions")
print("row 2 (pizza):", matrix[2])
print("column 1 (food-ness of every item):", matrix[:, 1])

# 4) Broadcasting: compare ONE query against EVERY row at once
query = np.array([0.85, 0.15, 0.3])   # something cat/dog-like
differences = matrix - query
print("\nmatrix - query (one row per item):")
for item, row in zip(items, differences):
    print(f"   {item:<6} {np.round(row, 2)}")

# 5) float32: half the memory of the default float64
small = matrix.astype(np.float32)
print("\nfloat64 bytes:", matrix.nbytes, "| float32 bytes:", small.nbytes)
