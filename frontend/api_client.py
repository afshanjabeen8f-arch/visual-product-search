"""
api_client.py
--------------
This file is responsible for ONE thing only: talking to Person 2's
backend and converting its response into the exact shape that
frontend/app.py expects.

app.py expects search_similar_products(image) to return a LIST of
dictionaries that look like this:

    {
        "name": "...",
        "price": 0.0,
        "category": "...",
        "similarity": ...,
        "image": "http://..."
    }

The backend currently returns something different (see BACKEND_URL /search
below), so this file's job is to "translate" between the two shapes.
"""

import requests

# -----------------------------
# Backend configuration
# -----------------------------
# Base URL where Person 2's backend is running locally.
BACKEND_BASE_URL = "http://127.0.0.1:8000"

# Full URL of the search endpoint we send the uploaded image to.
SEARCH_ENDPOINT = f"{BACKEND_BASE_URL}/search"

# How long (in seconds) we wait for the backend to respond before
# giving up. Prevents the app from freezing forever if the backend
# is stuck or unreachable.
REQUEST_TIMEOUT_SECONDS = 15


def search_similar_products(image):
    """
    Sends the uploaded image to the backend's /search endpoint and
    returns a list of product dictionaries in the format app.py expects.

    Parameters
    ----------
    image : an uploaded file object from st.file_uploader (in app.py)

    Returns
    -------
    list[dict]
        A list of products shaped for app.py's render_product_card().
        Returns an empty list if something goes wrong, and shows a
        Streamlit-friendly error via a raised exception that app.py
        already catches with its try/except block.
    """

    # -----------------------------
    # 1. Send the image to the backend
    # -----------------------------
    # requests expects files as a dict: {form_field_name: (filename, file_bytes, content_type)}
    # The backend expects the form field to be called "file".
    files = {
        "file": (image.name, image.getvalue(), image.type)
    }

    try:
        response = requests.post(
            SEARCH_ENDPOINT,
            files=files,
            timeout=REQUEST_TIMEOUT_SECONDS
        )

    except requests.exceptions.ConnectionError:
        # This happens when the backend server isn't running at all,
        # or the URL/port is wrong.
        raise Exception(
            f"Could not connect to the backend at {BACKEND_BASE_URL}. "
            "Please make sure the backend server is running."
        )

    except requests.exceptions.Timeout:
        # The backend took too long to respond.
        raise Exception(
            f"The backend did not respond within {REQUEST_TIMEOUT_SECONDS} seconds. "
            "Please try again."
        )

    except requests.exceptions.RequestException as e:
        # Catch-all for any other networking problem (DNS issues, etc).
        raise Exception(f"An unexpected network error occurred: {e}")

    # -----------------------------
    # 2. Check for HTTP errors (e.g. 404, 500)
    # -----------------------------
    # raise_for_status() raises an exception automatically if the
    # backend returned a non-2xx status code (like 500 Internal Server Error).
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        raise Exception(f"The backend returned an error: {e}")

    # -----------------------------
    # 3. Parse the JSON response
    # -----------------------------
    try:
        response_data = response.json()
    except ValueError:
        # This happens if the backend response isn't valid JSON at all.
        raise Exception("The backend returned an invalid (non-JSON) response.")

    # -----------------------------
    # 4. Validate the expected structure
    # -----------------------------
    # We expect: {"results": [ {...}, {...}, ... ]}
    raw_results = response_data.get("results")

    if raw_results is None:
        raise Exception(
            "The backend response was missing the expected 'results' field."
        )

    # -----------------------------
    # 5. Convert each backend product into app.py's expected format
    # -----------------------------
    converted_products = []

    for item in raw_results:
        # Build the full/absolute image URL.
        # Backend gives us something like "/images/1164.jpg".
        # We need "http://127.0.0.1:8000/images/1164.jpg" so the
        # browser can actually load it.
        relative_image_path = item.get("image_url", "")
        full_image_url = f"{BACKEND_BASE_URL}{relative_image_path}" if relative_image_path else ""

        converted_product = {
            "name": item.get("name", "Unknown Product"),
            "price": item.get("price", 0),
            "category": item.get("category", "N/A"),

            # IMPORTANT: The backend does NOT currently return a real
            # similarity score. We deliberately do NOT invent a fake
            # number here, because that would misrepresent the ML
            # model's actual output.
            #
            # We use None as a clearly-documented placeholder.
            # NOTE: app.py's existing code treats a non-numeric
            # similarity as 0 (it wasn't built to show "N/A" — and per
            # this task's scope, app.py is not being modified). So
            # until Person 2's backend adds a real similarity score,
            # cards will display "0% Match" as a known, temporary
            # limitation — NOT a real model output.
            "similarity": None,

            "image": full_image_url,
        }

        converted_products.append(converted_product)

    return converted_products