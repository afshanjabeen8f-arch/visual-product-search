"""
frontend/api_client.py

Connects the Streamlit frontend to the real backend at
http://127.0.0.1:8000/search instead of using mock_data.py.
"""

import requests

BASE_URL = "http://127.0.0.1:8000"
SEARCH_ENDPOINT = f"{BASE_URL}/search"
IMAGE_BASE_URL = BASE_URL  # backend returns paths like /images/1542.jpg
REQUEST_TIMEOUT = 15  # seconds


def _build_image_url(relative_url):
    """Convert '/images/1542.jpg' -> 'http://127.0.0.1:8000/images/1542.jpg'."""
    if not relative_url:
        return None
    if relative_url.startswith("http://") or relative_url.startswith("https://"):
        return relative_url
    if not relative_url.startswith("/"):
        relative_url = "/" + relative_url
    return f"{IMAGE_BASE_URL}{relative_url}"


def _convert_result(item):
    """Convert one backend result dict into the shape app.py expects."""
    return {
        "name": item.get("name", "Unknown product"),
        "price": item.get("price"),
        "category": item.get("category"),
        # Backend does not return a similarity score yet — never fake one.
        "similarity": item.get("similarity"),
        "image": _build_image_url(item.get("image_url")),
        # Extra fields preserved for optional use in app.py; harmless if unused.
        "color": item.get("color"),
        "gender": item.get("gender"),
        "product_id": item.get("product_id"),
    }


def search_similar_products(uploaded_image):
    """
    Send the uploaded Streamlit image to POST /search and return a list of
    product dicts in the format app.py expects:

        {"name", "price", "category", "similarity", "image", "color", "gender"}

    On any failure, returns an empty list and the caller (app.py) can check
    st.session_state / the return value's length to show a message — nothing
    here calls st.* directly so this stays testable outside Streamlit.

    Raises no exceptions to the caller; instead attaches a human-readable
    error message as `search_similar_products.last_error` for app.py to show
    if desired.
    """
    search_similar_products.last_error = None

    if uploaded_image is None:
        search_similar_products.last_error = "No image was provided."
        return []

    try:
        # uploaded_image is a Streamlit UploadedFile (from st.file_uploader)
        file_bytes = uploaded_image.getvalue()
        filename = getattr(uploaded_image, "name", "upload.jpg")
        content_type = getattr(uploaded_image, "type", "application/octet-stream")

        files = {"file": (filename, file_bytes, content_type)}
        response = requests.post(SEARCH_ENDPOINT, files=files, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()

    except requests.exceptions.ConnectionError:
        search_similar_products.last_error = (
            "Could not connect to the backend. Is it running at "
            f"{BASE_URL}?"
        )
        return []
    except requests.exceptions.Timeout:
        search_similar_products.last_error = (
            "The backend took too long to respond (timeout)."
        )
        return []
    except requests.exceptions.HTTPError as e:
        search_similar_products.last_error = f"Backend returned an error: {e}"
        return []
    except requests.exceptions.RequestException as e:
        search_similar_products.last_error = f"Request to backend failed: {e}"
        return []

    try:
        data = response.json()
    except ValueError:
        search_similar_products.last_error = "Backend response was not valid JSON."
        return []

    results = data.get("results", [])
    if not results:
        search_similar_products.last_error = "No matching products were found."
        return []

    return [_convert_result(item) for item in results]


# Default so app.py can safely read this even before a search has been run.
search_similar_products.last_error = None