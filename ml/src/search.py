import json
import numpy as np
import faiss
from embedding_generator import get_embedding

INDEX_PATH = "data/faiss_index.bin"
IDS_PATH = "data/product_ids.json"


def search_similar_products(image_path, top_k=5):
    """
    Takes a path to a query image, returns the top_k most visually similar products.
    Output format: [{"product_id": ..., "score": ...}, ...]
    """
    # Step 1: turn the query image into an embedding (same pipeline as before)
    query_embedding = get_embedding(image_path)
    query_embedding = np.array([query_embedding]).astype("float32")  # FAISS expects a 2D array

    # Step 2: load the saved FAISS index and product ID list
    index = faiss.read_index(INDEX_PATH)
    with open(IDS_PATH, "r") as f:
        product_ids = json.load(f)

    # Step 3: search — returns distances and row numbers of the closest matches
    distances, row_numbers = index.search(query_embedding, top_k)

    # Step 4: translate row numbers back into actual product IDs
    results = []
    for distance, row_number in zip(distances[0], row_numbers[0]):
        product_id = product_ids[row_number]
        results.append({"product_id": product_id, "score": float(distance)})

    return results


# Quick test
if __name__ == "__main__":
    test_image =  "dataset/products/1164.jpg" # try searching using one of our own images first
    results = search_similar_products(test_image, top_k=5)

    print("Top matches:")
    for r in results:
        print(r)