# ML Component — Visual Product Search

## What this does
Given a product image, returns the top-K most visually similar products from our dataset, using a pretrained CNN (ResNet-18) for feature extraction and FAISS for similarity search.

## Setup
1. Install dependencies:
   pip install -r requirements.txt
2. Make sure these 3 files are inside a `data/` folder:
   - embeddings.npy
   - product_ids.json
   - faiss_index.bin
   (Already sent separately — these are generated files, not in Git.)

## How to call it
```python
from search import search_similar_products

results = search_similar_products("path/to/image.jpg", top_k=5)
```

## Input
- `image_path` (string): path to an image file (.jpg, .jpeg, .png)
- `top_k` (int, optional, default 5): how many similar products to return

## Output
A list of dictionaries, ordered from most to least similar:
```python
[
  {"product_id": "1164", "score": 0.0},
  {"product_id": "1909", "score": 156.13},
  ...
]
```
- `product_id`: matches the filename (without extension) in `dataset/products/`
- `score`: distance (lower = more similar). Not a percentage — just use it for ordering.

## Important note for backend/frontend
This function only returns `product_id` and `score` — no name, price, image, or category.
To show full product details, map `product_id` against `styles.csv` (from the Kaggle
"Fashion Product Images (Small)" dataset) — this lookup step needs to happen in the backend,
since this ML function has no knowledge of product metadata.

## Error handling
If the image path is invalid or unreadable, this raises a `ValueError` with a clear message.
Wrap calls in try/except:
```python
try:
    results = search_similar_products(image_path)
except ValueError as e:
    # handle gracefully, e.g. return an error response to frontend
    print(e)
```

## Files needed from this repo
- `src/preprocess.py`
- `src/feature_extractor.py`
- `src/embedding_generator.py`
- `src/search.py`
- `requirements.txt`