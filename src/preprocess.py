from PIL import Image
from torchvision import transforms

# This defines the exact standardization steps, in order
preprocess_pipeline = transforms.Compose([
    transforms.Resize((224, 224)),      # force every image to 224x224 pixels
    transforms.ToTensor(),              # convert image to a tensor (a grid of numbers)
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
        image = Image.open(image_path).convert("RGB")  # open + force 3 color channels
    except Exception as e:
        raise ValueError(f"Could not open image at {image_path}: {e}")

    image_tensor = preprocess_pipeline(image)   # apply resize + tensor + normalize
    image_tensor = image_tensor.unsqueeze(0)    # add a "batch" dimension (explained below)

    return image_tensor


# Quick test — only runs if you execute this file directly
if __name__ == "__main__":
    test_path = "dataset/products/product_001.jpg"   # change this to a real filename you have
    tensor = load_and_preprocess_image("dataset/products/1164.jpg")
    print("Success! Tensor shape:", tensor.shape)