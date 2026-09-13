import json
import sys
from pathlib import Path

import faiss
import numpy as np


# --------------------------------------------------
# Project paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

INDEX_PATH = BASE_DIR / "ml" / "faiss_index.bin"
PRODUCT_IDS_PATH = BASE_DIR / "ml" / "product_ids.json"

ML_SRC_PATH = BASE_DIR / "ml" / "src"

# Allow us to import Person 1's ML code
sys.path.insert(0, str(ML_SRC_PATH))

from embedding_generator import get_embedding


# --------------------------------------------------
# Load FAISS index and product IDs
# --------------------------------------------------

index = faiss.read_index(str(INDEX_PATH))

with open(PRODUCT_IDS_PATH, "r") as f:
    product_ids = json.load(f)


# --------------------------------------------------
# Search using an embedding
# --------------------------------------------------

def search_similar(query_embedding, k=5):

    query_embedding = np.asarray(
        query_embedding,
        dtype="float32"
    ).reshape(1, -1)

    distances, indices = index.search(query_embedding, k)
    print("FAISS distances:", distances[0])
    results = []

    valid_distances = [
        float(distance)
        for distance, idx in zip(distances[0], indices[0])
        if idx >= 0
    ]

    if not valid_distances:
        return results
    
# Convert distances into a smooth, demo-friendly similarity score.
    # Smaller FAISS distance = more similar.
    #
    # Similarity decreases smoothly as the distance gets farther
    # from the nearest result.
    min_distance = min(valid_distances)
    max_distance = max(valid_distances)

    scale = max_distance - min_distance

    if scale == 0:
        scale = 1e-6  # avoid divide-by-zero when all distances are equal

    for distance, idx in zip(distances[0], indices[0]):

        if idx < 0:
            continue

        distance = float(distance)

        similarity = 100.0 * np.exp(
            -(distance - min_distance) / scale
        )

        similarity = max(0.0, min(similarity, 100.0))
    
        results.append({
            "product_id": product_ids[idx],
            "similarity": round(similarity, 2)
        })

    return results 


# --------------------------------------------------
# Search using an image
# --------------------------------------------------

def search_image(image_path, k=5):

    # Generate the 512-dimensional embedding
    embedding = get_embedding(str(image_path))

    # Search FAISS
    return search_similar(embedding, k)