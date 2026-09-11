import os
import numpy as np
import json
from embedding_generator import get_embedding

PRODUCTS_FOLDER = "dataset/products"
EMBEDDINGS_OUTPUT_PATH = "data/embeddings.npy"
IDS_OUTPUT_PATH = "data/product_ids.json"


def build_all_embeddings():
    all_embeddings = []
    all_product_ids = []

    image_files = [f for f in os.listdir(PRODUCTS_FOLDER) if f.lower().endswith((".jpg", ".jpeg", ".png"))]

    if len(image_files) == 0:
        raise ValueError(f"No images found in {PRODUCTS_FOLDER}. Did you add your product images?")

    for filename in image_files:
        image_path = os.path.join(PRODUCTS_FOLDER, filename)
        product_id = os.path.splitext(filename)[0]   # e.g. "1164.jpg" -> "1164"

        try:
            embedding = get_embedding(image_path)
        except Exception as e:
            print(f"Skipping {filename} due to error: {e}")
            continue

        all_embeddings.append(embedding)
        all_product_ids.append(product_id)
        print(f"Processed {filename} -> product_id: {product_id}")

    # Stack all embeddings into one big 2D array: (num_products, 512)
    embeddings_array = np.stack(all_embeddings)

    # Save embeddings as a .npy file (NumPy's own fast binary format)
    np.save(EMBEDDINGS_OUTPUT_PATH, embeddings_array)

    # Save product IDs as a simple JSON list, in the SAME order as the embeddings
    with open(IDS_OUTPUT_PATH, "w") as f:
        json.dump(all_product_ids, f)

    print(f"\nDone! Saved {len(all_product_ids)} embeddings.")
    print(f"Embeddings shape: {embeddings_array.shape}")


if __name__ == "__main__":
    build_all_embeddings()