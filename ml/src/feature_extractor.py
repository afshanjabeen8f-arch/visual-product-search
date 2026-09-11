import torch
import torchvision.models as models
import torch.nn as nn

# Load ResNet-18 with pretrained weights (already trained on millions of images)
resnet = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)

# Remove the final classification layer.
# nn.Identity() means "just pass the data through unchanged" instead of classifying it.
resnet.fc = nn.Identity()  # type: ignore[assignment]

# Tell PyTorch we are NOT training this model — just using it as-is.
resnet.eval()


def extract_embedding(image_tensor):
    """
    Takes a preprocessed image tensor, returns its embedding (feature vector).
    """
    with torch.no_grad():   # no_grad = don't waste time/memory tracking training info
        embedding = resnet(image_tensor)

    return embedding


# Quick test
if __name__ == "__main__":
    from preprocess import load_and_preprocess_image

    test_path = "dataset/products/1164.jpg"
    tensor = load_and_preprocess_image(test_path)

    embedding = extract_embedding(tensor)
    print("Embedding shape:", embedding.shape)