import numpy as np
from preprocess import load_and_preprocess_image
from feature_extractor import extract_embedding


def get_embedding(image_path):
    """
    Full pipeline: image path -> preprocessed tensor -> embedding (as a plain numpy array).
    """
    tensor = load_and_preprocess_image(image_path)
    embedding_tensor = extract_embedding(tensor)

    # Convert from PyTorch tensor to a plain numpy array, and remove the "batch" dimension
    embedding_array = embedding_tensor.squeeze(0).numpy()

    return embedding_array


# Quick test
if __name__ == "__main__":
    test_path = "dataset/products/1164.jpg"
    embedding = get_embedding(test_path)

    print("Embedding shape:", embedding.shape)
    print("First 5 numbers:", embedding[:5])