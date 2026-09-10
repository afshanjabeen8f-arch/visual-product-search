import numpy as np
import faiss

EMBEDDINGS_PATH = "data/embeddings.npy"
INDEX_OUTPUT_PATH = "data/faiss_index.bin"


def build_faiss_index():
    # Load the embeddings we saved in Stage 5
    embeddings = np.load(EMBEDDINGS_PATH)
    embeddings = embeddings.astype("float32")   # FAISS requires float32, not float64

    num_products, embedding_dim = embeddings.shape
    print(f"Loaded {num_products} embeddings, each with {embedding_dim} numbers.")

    # Create a FAISS index that compares using L2 (straight-line) distance
    index = faiss.IndexFlatL2(embedding_dim)

    # Add all our product embeddings into the index
    index.add(embeddings)

    print(f"Index now contains {index.ntotal} vectors.")

    # Save the index to disk so we don't have to rebuild it every time
    faiss.write_index(index, INDEX_OUTPUT_PATH)
    print(f"Saved index to {INDEX_OUTPUT_PATH}")


if __name__ == "__main__":
    build_faiss_index()