# Hand-made 2-number "embeddings": (animal-ness, food-ness), each from 0.0 to 1.0
WORDS = {
    "cat": (0.9, 0.1),
    "dog": (0.8, 0.2),
    "pizza": (0.1, 0.9),
    "burger": (0.2, 0.8),
    "chicken": (0.6, 0.6),
}

GRID_SIZE = 11  # positions 0..10 on each axis, one per 0.1 step

# Start with an empty grid of dots
grid = [["." for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# Place each word on the grid using its two numbers as coordinates
for number, (word, (animal, food)) in enumerate(WORDS.items(), start=1):
    column = round(animal * 10)
    row = round(food * 10)
    grid[row][column] = str(number)
    print(f"{number} = {word:<8} animal-ness {animal}, food-ness {food}")

# Draw it, highest food-ness at the top
print("\nfood-ness")
for row in range(GRID_SIZE - 1, -1, -1):
    print(f"  {row / 10:.1f} | " + " ".join(grid[row]))
print("      +" + "-" * (GRID_SIZE * 2))
print("        0.0       0.5       1.0   animal-ness")
