import random
import sys
import time

import numpy as np

COUNT = 1_000          # how many "documents"
DIMENSIONS = 1536      # same size as a real embedding

random.seed(42)
documents_list = [[random.random() for _ in range(DIMENSIONS)] for _ in range(COUNT)]
query_list = [random.random() for _ in range(DIMENSIONS)]

documents_np = np.array(documents_list, dtype=np.float32)
query_np = np.array(query_list, dtype=np.float32)

# Task: subtract the query from every document (element-wise), then add up each row
start = time.perf_counter()
totals_list = [sum(d - q for d, q in zip(document, query_list)) for document in documents_list]
list_seconds = time.perf_counter() - start

start = time.perf_counter()
totals_np = (documents_np - query_np).sum(axis=1)
numpy_seconds = time.perf_counter() - start

print(f"Python lists: {list_seconds * 1000:8.1f} ms")
print(f"NumPy       : {numpy_seconds * 1000:8.1f} ms")
print(f"NumPy is about {list_seconds / numpy_seconds:,.0f}× faster")
print(f"Same answers? {np.allclose(totals_list, totals_np, atol=1e-2)}")

list_bytes = sum(sys.getsizeof(doc) + sum(sys.getsizeof(x) for x in doc) for doc in documents_list)
print(f"\nMemory for {COUNT:,} vectors:")
print(f"   Python lists  : {list_bytes / 1_000_000:6.1f} MB")
print(f"   NumPy float32 : {documents_np.nbytes / 1_000_000:6.1f} MB")
