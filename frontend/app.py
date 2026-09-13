import streamlit as st
from api_client import search_similar_products

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Visual Product Search & Recommendation Engine",
    page_icon="🛍️",
    layout="wide"
)

# -----------------------------
# Custom CSS Styling
# -----------------------------
st.markdown("""
    <style>
    .main-title {
        font-size: 2.5rem;
        font-weight: 800;
        color: #1a1a1a;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1.05rem;
        color: #6b7280;
        margin-bottom: 1.5rem;
    }
    .section-header {
        font-size: 1.6rem;
        font-weight: 700;
        margin-top: 1.5rem;
        margin-bottom: 0.3rem;
        color: #1a1a1a;
        border-left: 5px solid #4F46E5;
        padding-left: 10px;
    }
    .section-caption {
        font-size: 0.95rem;
        color: #6b7280;
        margin-bottom: 1.2rem;
        padding-left: 15px;
    }
    .upload-heading {
        font-size: 1.3rem;
        font-weight: 700;
        color: #1a1a1a;
        margin-top: 0.5rem;
        margin-bottom: 0.8rem;
        text-align: center;
    }
    /* Filter Section */
    .filter-box {
        background-color: #F9FAFB;
        border: 1px solid #E5E7EB;
        border-radius: 16px;
        padding: 20px 20px 5px 20px;
        margin-bottom: 1.5rem;
    }
    .filter-heading {
        font-size: 1.15rem;
        font-weight: 700;
        color: #1a1a1a;
        margin-bottom: 0.8rem;
    }
    .match-count {
        font-size: 0.9rem;
        color: #4F46E5;
        font-weight: 600;
        margin-top: 0.3rem;
        margin-bottom: 1rem;
    }
    /* Product Card */
    .product-card {
        background-color: #ffffff;
        border-radius: 18px;
        padding: 18px;
        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.07);
        text-align: center;
        margin-bottom: 28px;
        border: 1px solid #f0f0f0;
        transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
    }
    .product-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 6px 18px rgba(79, 70, 229, 0.15);
    }
    .product-image-wrapper {
        width: 100%;
        height: 220px;
        border-radius: 14px;
        overflow: hidden;
        margin-bottom: 12px;
        background-color: #f5f5f5;
    }
    .product-image-wrapper img {
        width: 100%;
        height: 100%;
        object-fit: contain;
        display: block;
    }
    .similar-label {
        display: inline-block;
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        color: #4F46E5;
        background-color: #EEF2FF;
        padding: 2px 10px;
        border-radius: 12px;
        margin-bottom: 8px;
    }
    .product-name {
        font-size: 1.1rem;
        font-weight: 700;
        color: #1a1a1a;
        margin-top: 4px;
    }
    .product-category {
        font-size: 0.85rem;
        color: #9ca3af;
        margin-bottom: 8px;
    }
    .product-price {
        font-size: 1.15rem;
        font-weight: 700;
        color: #4F46E5;
        margin-bottom: 10px;
    }
    .similarity-badge {
        display: inline-block;
        background-color: #EEF2FF;
        color: #4F46E5;
        font-weight: 700;
        padding: 4px 14px;
        border-radius: 20px;
        font-size: 0.9rem;
        margin-bottom: 8px;
    }
    /* Custom progress bar for similarity */
    .similarity-bar-bg {
        width: 100%;
        background-color: #E5E7EB;
        border-radius: 10px;
        height: 8px;
        margin-top: 4px;
        overflow: hidden;
    }
    .similarity-bar-fill {
        height: 100%;
        background-color: #4F46E5;
        border-radius: 10px;
    }
    .empty-state {
        text-align: center;
        padding: 60px 20px;
        color: #9ca3af;
        font-size: 1.1rem;
    }
    .no-match-state {
        text-align: center;
        padding: 40px 20px;
        color: #9ca3af;
        font-size: 1.05rem;
        background-color: #F9FAFB;
        border-radius: 14px;
        border: 1px dashed #E5E7EB;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------
# Session State Initialization
# -----------------------------
# We store the search results here so they survive Streamlit reruns
# that happen when the user changes a filter widget (slider/selectbox).
if "search_results" not in st.session_state:
    st.session_state.search_results = None  # No search performed yet

# -----------------------------
# Header Section
# -----------------------------
st.markdown('<div class="main-title">🛍️ Visual Product Search & Recommendation Engine</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">Upload a product image and discover visually similar items instantly. '
    'This system analyzes the visual features of your image to recommend matching products from our catalog.</div>',
    unsafe_allow_html=True
)

st.divider()

# -----------------------------
# Upload Section
# -----------------------------
st.markdown('<div class="section-header">📤 Upload a Product Image</div>', unsafe_allow_html=True)
st.write("Supported formats: **JPG, JPEG, PNG**. For best results, upload a clear image of a single product.")

uploaded_image = st.file_uploader(
    "Choose an image file",
    type=["jpg", "jpeg", "png"]
)

# Show a clean, centered preview of the uploaded image
if uploaded_image is not None:
    st.markdown('<div class="upload-heading">🖼️ Your Uploaded Product</div>', unsafe_allow_html=True)
    _, preview_col, _ = st.columns([1, 1.2, 1])
    with preview_col:
        st.image(uploaded_image, caption="Uploaded Image Preview", use_container_width=True)

st.write("")  # spacing

# -----------------------------
# Search Button
# -----------------------------
search_clicked = st.button(
    "🔍 Search Similar Products",
    disabled=(uploaded_image is None),
    use_container_width=False
)

st.divider()


# -----------------------------
# Helper function to render one product card
# -----------------------------
def render_product_card(product):
    """Builds and displays a single styled product card using HTML/CSS."""
    name = product.get("name", "Unknown Product")
    category = product.get("category", "N/A")
    price = product.get("price", 0)
    similarity = product.get("similarity")
    image_url = product.get("image", "")

    # Backend already returns a 0-100 similarity score.
    # Do not calculate it again in the frontend.
    if similarity is None:
        similarity_value = None
    else:
        try:
            similarity_value = float(similarity)
        except (ValueError, TypeError):
            similarity_value = None

    if similarity_value is None:
        match_label = "Match: N/A"
        similarity_bar_html = ""
    else:
        # Keep the score safely between 0 and 100.
        similarity_percent = max(0, min(similarity_value, 100))
        match_label = f"{similarity_percent:.2f}% Match"

        similarity_bar_html = (
            f'<div class="similarity-bar-bg">'
            f'<div class="similarity-bar-fill" '
            f'style="width:{similarity_percent}%;"></div>'
            f'</div>'
        )

    card_html = f"""
<div class="product-card">
    <div class="similar-label">Visually Similar</div>
    <div class="product-image-wrapper">
        <img src="{image_url}" alt="{name}">
    </div>
    <div class="product-name">{name}</div>
    <div class="product-category">{category}</div>
    <div class="product-price">₹{price:.2f}</div>
    <div class="similarity-badge">{match_label}</div>
    {similarity_bar_html}
</div>
"""
    st.markdown(card_html, unsafe_allow_html=True)


def render_products_in_rows(products_to_show):
    """Displays products in a 3-column row followed by a centered 2-column row."""
    # ---- Row 1: first 3 products in 3 columns ----
    first_row = products_to_show[:3]
    if first_row:
        row1_cols = st.columns(len(first_row))
        for col, product in zip(row1_cols, first_row):
            with col:
                render_product_card(product)

    # ---- Row 2: remaining products in 2 centered columns ----
    second_row = products_to_show[3:5]
    if second_row:
        if len(second_row) == 2:
            spacer_left, col_a, col_b, spacer_right = st.columns([1, 2, 2, 1])
            row2_cols = [col_a, col_b]
        else:
            spacer_left, col_a, spacer_right = st.columns([1, 2, 1])
            row2_cols = [col_a]
        for col, product in zip(row2_cols, second_row):
            with col:
                render_product_card(product)


# -----------------------------
# Run a new search when the button is clicked
# -----------------------------
if search_clicked and uploaded_image is not None:
    try:
        # Show a spinner while "searching"
        with st.spinner("Analyzing image and finding similar products..."):
            products = search_similar_products(uploaded_image)

        # Store the results in session_state so they persist across
        # future reruns (e.g. when filters are changed).
        st.session_state.search_results = products

    except Exception as e:
        # Graceful handling of unexpected errors
        st.error(f"Something went wrong while searching for products: {e}")
        st.session_state.search_results = None

# -----------------------------
# Results Section
# -----------------------------
if uploaded_image is None:
    # Friendly empty state before upload
    st.markdown(
        '<div class="empty-state">👋 Upload a product image above to get started.<br>'
        'Your top 5 visually similar products will appear here.</div>',
        unsafe_allow_html=True
    )

elif st.session_state.search_results is None:
    # Image uploaded but no search performed yet
    st.info("Click the **Search Similar Products** button to view recommendations.")

else:
    products = st.session_state.search_results

    if not products:
        # Handle case where no products were returned by the search
        st.warning("No similar products were found. Please try a different image.")
    else:
        # -----------------------------
        # Build filter options dynamically from the stored products
        # -----------------------------
        available_categories = sorted(
            {product.get("category", "Unknown") for product in products}
        )
        category_options = ["All Categories"] + available_categories

        prices = [float(product.get("price", 0)) for product in products]
        min_price = min(prices) if prices else 0
        max_price = max(prices) if prices else 100

        # Whether any product actually has a similarity score yet.
        has_similarity_data = any(
            product.get("similarity") is not None for product in products
        )

        # -----------------------------
        # Filter Section UI
        # -----------------------------
        # Because "products" now comes from session_state instead of a
        # local variable, changing these widgets triggers a rerun that
        # still has access to the same search results.
        st.markdown('<div class="filter-box">', unsafe_allow_html=True)
        st.markdown('<div class="filter-heading">🔧 Filter Results</div>', unsafe_allow_html=True)

        filter_col1, filter_col2, filter_col3 = st.columns(3)

        with filter_col1:
            selected_category = st.selectbox(
                "Category",
                options=category_options,
                index=0
            )

        with filter_col2:
            selected_max_price = st.slider(
                "Maximum Price (₹)",
                min_value=float(min_price),
                max_value=float(max_price),
                value=float(max_price)
            )

        with filter_col3:
            if has_similarity_data:
                selected_min_similarity = st.slider(
                    "Minimum Similarity (%)",
                    min_value=0,
                    max_value=100,
                    value=0
                )
            else:
                selected_min_similarity = None
                st.markdown("**Minimum Similarity (%)**")
                st.caption("Not available yet — the backend doesn't return a similarity score.")

        st.markdown('</div>', unsafe_allow_html=True)

        # -----------------------------
        # Apply filters to the product list stored in session_state
        # -----------------------------
        filtered_products = []
        for product in products:
            product_category = product.get("category", "Unknown")
            product_price = float(product.get("price", 0))

            raw_similarity = product.get("similarity")
            if raw_similarity is None:
                # No similarity data for this product — never let the
                # similarity filter exclude it.
                similarity_match = True
            else:
                try:
                    product_similarity = float(raw_similarity)
                except (ValueError, TypeError):
                    product_similarity = None

                if product_similarity is None or selected_min_similarity is None:
                    similarity_match = True
                else:
                    similarity_match = product_similarity >= selected_min_similarity

            # Category check (skip check if "All Categories" is selected)
            category_match = (
                selected_category == "All Categories"
                or product_category == selected_category
            )

            # Price check
            price_match = product_price <= selected_max_price

            if category_match and price_match and similarity_match:
                filtered_products.append(product)

        # -----------------------------
        # Results Heading
        # -----------------------------
        st.markdown('<div class="section-header">✨ Top Similar Products</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="section-caption">These are the products most visually similar to your uploaded image.</div>',
            unsafe_allow_html=True
        )

        # Show how many products match the current filters
        st.markdown(
            f'<div class="match-count">Showing {len(filtered_products)} of {len(products)} products matching your filters.</div>',
            unsafe_allow_html=True
        )

        # -----------------------------
        # Display filtered products or a friendly "no match" message
        # -----------------------------
        if not filtered_products:
            st.markdown(
                '<div class="no-match-state">😕 No products match your current filters. '
                'Try adjusting them.</div>',
                unsafe_allow_html=True
            )
        else:
            render_products_in_rows(filtered_products[:5])