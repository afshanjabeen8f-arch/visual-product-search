# Visual Product Search & Recommendation

This project lets a user upload a photo of a product and get back a list of visually similar products from our catalog, instead of searching by typing keywords.

It uses a pretrained ResNet-18 model to turn images into feature vectors (embeddings), and FAISS to quickly find which stored products are most similar to the uploaded image. A FastAPI backend handles the requests, and a Streamlit app provides the user interface.

---

## How It Works

1. The user uploads a product image through the Streamlit app.
2. The image is sent to the FastAPI backend's `/search` endpoint.
3. The backend preprocesses the image (resize, normalize) and passes it through ResNet-18 to get a 512-number feature vector.
4. FAISS compares this vector against all stored product embeddings and returns the top 5 closest matches, along with a similarity score.
5. The backend looks up each matched product's name, price, category, color, and gender from `products.csv`.
6. The final result (product details + similarity scores) is sent back to the frontend and displayed to the user.

---

## Features

- Search by image instead of keywords
- Visual feature extraction using a pretrained ResNet-18 (no training from scratch — just reusing what it already learned)
- FAISS-based similarity search
- Returns the top 5 most similar products, ranked by similarity
- Product details (name, category, color, gender, demo price) attached to each result
- FastAPI backend with automatic Swagger docs for testing
- Streamlit frontend for uploading images and viewing results

---

## Tech Stack

| Technology  | Used For                             |
| ----------- | ------------------------------------- |
| Python      | Main language                         |
| PyTorch     | Deep learning framework               |
| Torchvision | ResNet-18 model + image transforms    |
| ResNet-18   | Feature extraction (transfer learning)|
| FAISS       | Similarity search                     |
| NumPy       | Numerical operations                  |
| Pandas      | Reading/handling product metadata     |
| Pillow      | Image loading                         |
| FastAPI     | Backend API                           |
| Uvicorn     | Running the FastAPI server            |
| Streamlit   | Frontend UI                           |

---

## Dataset

We used the **Fashion Product Images (Small)** dataset from Kaggle:
https://www.kaggle.com/datasets/paramaggarwal/fashion-product-images-small

The full dataset has around 44,000 fashion product images with metadata (category, color, gender, etc.). For this project, we picked 30 product images to build a working prototype.

- Product images: `dataset/products/`
- Product metadata: `products/products.csv`

Note: the original dataset doesn't include prices. The prices shown in this project are demo values we added ourselves, just for the prototype — not real prices.

---

## Machine Learning Part (Aleenamehreen04)

**Preprocessing** (`ml/src/preprocess.py`)
Every image is converted to RGB, resized to 224x224, turned into a tensor, and normalized using standard ImageNet values. This matches what ResNet-18 expects as input.

**Feature extraction** (`ml/src/feature_extractor.py`)
We load a pretrained ResNet-18 and remove its final classification layer, replacing it with `nn.Identity()`. This means instead of predicting a class label, the model just gives us the 512-number vector it would have used to make that prediction. The model runs in `eval()` mode since we're not training it.

**Embedding generation** (`ml/src/embedding_generator.py`)
Combines preprocessing and feature extraction into one function:

```python
get_embedding(image_path)   # image path in, 512-number embedding out
```

This same function is used both when building the product catalog and when processing a new search image, so both go through identical steps.

**Building the product database** (`ml/src/build_dataset_embeddings.py`)
Runs `get_embedding()` on every product image and saves two files:
- `embeddings.npy` — all embeddings stacked together
- `product_ids.json` — the product ID for each row, in the same order, so we can match a result back to an actual product

**FAISS index** (`ml/src/build_faiss_index.py`)
Builds a FAISS index (`IndexFlatL2`, using straight-line/L2 distance) from the saved embeddings and saves it to disk, so it doesn't need to be rebuilt every time someone searches.

**Search function** (`ml/src/search.py`)

```python
def search_similar_products(image_path, top_k=5):
    # Input: path to an image file, and how many results to return
    # Output: [{"product_id": "1164", "score": 0.0}, ...]
    #   ordered from most to least similar
    #   score is a distance, so lower = more similar
    # Raises ValueError if the image can't be opened
```

This function only knows about visual similarity — it has no idea what a product is called or how much it costs. That part comes from the backend.

---

## Project Structure

visual-product-search/
├── backend/
│ ├── app.py (FastAPI app and endpoints)
│ └── search.py (calls the ML search function)
├── frontend/
│ ├── app.py (Streamlit UI)
│ ├── api_client.py (talks to the backend)
│ └── mock_data.py
├── dataset/
│ └── products/ (30 product images, named by product ID)
├── ml/
│ ├── embeddings.npy
│ ├── faiss_index.bin
│ ├── product_ids.json
│ └── src/
│ ├── preprocess.py
│ ├── feature_extractor.py
│ ├── embedding_generator.py
│ ├── build_dataset_embeddings.py
│ ├── build_faiss_index.py
│ └── search.py
├── products/
│ └── products.csv (product names, prices, categories)
├── styles.csv (original Kaggle metadata)
├── requirements.txt
└── README.md


---

## How to Run It

1. Clone the repo:
```bash
git clone https://github.com/afshanjabeen8f-arch/visual-product-search.git
cd visual-product-search
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
venv\Scripts\Activate.ps1
```

3. Install the requirements:
```bash
pip install -r requirements.txt
```

4. Start the backend (in one terminal):
```bash
uvicorn backend.app:app --reload
```
Runs at `http://127.0.0.1:8000`. Swagger docs at `http://127.0.0.1:8000/docs`.

5. Start the frontend (in a second terminal, keep the backend running):
```bash
streamlit run frontend/app.py
```

---

## API Endpoints

| Method | Endpoint    | What it does                        |
|--------|-------------|--------------------------------------|
| GET    | `/`         | Checks if the API is running        |
| GET    | `/products` | Returns the full product catalog    |
| POST   | `/search`   | Upload an image, get similar products |

Example request:
```bash
curl -X POST "http://127.0.0.1:8000/search" \
  -F "file=@1164.jpg;type=image/jpeg"
```

Example response:
```json
{
  "results": [
    {
      "product_id": "1164",
      "name": "Nike Men Blue T20 Indian Cricket Jersey",
      "category": "Tshirts",
      "color": "Blue",
      "gender": "Men",
      "price": 1999,
      "similarity": 0.0,
      "image_url": "/images/1164.jpg"
    }
  ]
}
```

---

## Who Did What

**Aleenamehreen04 — Machine Learning**
Image preprocessing, ResNet-18 feature extraction, embedding generation, FAISS index and search logic.

**afshanjabeen8f-arch — Backend**
FastAPI app, handling image uploads, connecting the ML search function to the API, adding product details and prices to the response.

**aroosa-fatima — Frontend**
Streamlit interface, image upload, calling the backend, and displaying the results with product images, names, and prices.

---

## Bugs We Found While Connecting Everything

When we connected all three parts together, we found two bugs that only showed up once things were actually talking to each other:

- The backend was calculating a similarity score internally but wasn't including it in the final response sent to the frontend — we added it back in.
- The frontend had a placeholder that always showed the similarity as "not available," left over from before the backend supported it — we updated it to actually read the value.

Each part worked fine on its own, but a couple of fields got dropped between them. Testing the whole thing end-to-end (not just each piece separately) is what caught this.

---

## Limitations

- Only 30 product images are used, not the full dataset
- Matches are based purely on visual similarity (color, shape, texture) — the model doesn't actually know what a product "is"
- Categories with very few example images (like bags, in our case) sometimes return unrelated-looking matches
- Prices are demo values, not real prices
- No personalization or purchase history is used

---

## What We'd Add Next

- More product images for better coverage across categories
- A bigger/more accurate vision model
- Filters for category, color, gender, price
- Real prices and product links
- Deploying it so it's publicly accessible

---

## Project Info

Project: Visual Product Search & Recommendation
Type: Team project (3 people)
Model used: ResNet-18 for feature extraction
Search: FAISS

---

## License

Built as an academic project. The Fashion Product Images (Small) dataset follows its own license on Kaggle.




https://github.com/user-attachments/assets/832feed1-2ac2-4ea4-82ec-30eefe83a6a8

