from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import shutil
import pandas as pd

from backend.search import search_image


app = FastAPI(title="Visual Product Search API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


BASE_DIR = Path(__file__).resolve().parent.parent

UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

PRODUCT_IMAGES_DIR = BASE_DIR / "dataset" / "products"

app.mount(
    "/images",
    StaticFiles(directory=str(PRODUCT_IMAGES_DIR)),
    name="images"
)


# Load product catalog
PRODUCTS_FILE = BASE_DIR / "products" / "products.csv"
products = pd.read_csv(PRODUCTS_FILE)

# Make sure IDs are strings
products["id"] = products["id"].astype(str)


@app.get("/")
def home():
    return {"message": "Visual Product Search API is running!"}


@app.get("/products")
def get_products():
    return {
        "products": products.to_dict(orient="records")
    }


@app.post("/search")
async def search(file: UploadFile = File(...)):

    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="Please upload an image file."
        )

    file_path = UPLOAD_DIR / (file.filename or "uploaded_image.jpg")

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        # Find visually similar products
        results = search_image(file_path, k=5)

        # Add product information
        final_results = []

        for result in results:

            product_id = str(result["product_id"])

            product = products[
                products["id"] == product_id
            ]

            if product.empty:
                continue

            product = product.iloc[0]

            final_results.append({
                "product_id": product_id,
                "name": product["productDisplayName"],
                "category": product["articleType"],
                "color": product["baseColour"],
                "gender": product["gender"],
                "image_url": f"/images/{product_id}.jpg",
                "similarity": result["similarity"],
                "price": float(product["price"])
            })

        return {
            "results": final_results
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    finally:
        if file_path.exists():
            file_path.unlink()