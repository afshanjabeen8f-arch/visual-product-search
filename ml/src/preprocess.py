from PIL import Image
from torchvision import transforms

# This defines the exact standardization steps, in order
preprocess_pipeline = transforms.Compose([
    transforms.Resize((224, 224)),      # force every image to 224x224 pixels
    transforms.ToTensor(),              # convert image to a tensor
    transforms.Normalize(               # scale numbers to what ResNet-18 expects
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])


def load_and_preprocess_image(image_path):
    """
    Takes a path to an image file, returns it ready for the CNN.
    """
    try:
        image = Image.open(image_path).convert("RGB")
    except Exception as e:
        raise ValueError(f"Could not open image at {image_path}: {e}")

    image_tensor = preprocess_pipeline(image)
    image_tensor = image_tensor.unsqueeze(0)  # type: ignore # add a "batch" dimension

    return image_tensor


# Quick test — only runs if you execute this file directly
if __name__ == "__main__":
    test_path = "dataset/products/1164.jpg"
    tensor = load_and_preprocess_image(test_path)
    print("Success! Tensor shape:", tensor.shape)