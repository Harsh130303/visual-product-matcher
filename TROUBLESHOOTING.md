# Development & Troubleshooting Log

This log tracks the technical challenges encountered during the development of the **Visual Product Matcher**, the solutions implemented, and the timeline of fixes. 

> [!NOTE]
> New issues and debugging steps will be appended to this log as they occur to maintain a complete project history.

## 📅 Session Date: 2026-02-22

### 00:11 - CSS Compatibility Issue
- **Problem**: Warning: `Also define the standard property 'background-clip' for compatibility`.
- **Cause**: Using the vendor-prefixed `-webkit-background-clip` without the standard CSS property.
- **Solution**: Added `background-clip: text;` to the `h1` selector in `index.css`.

### 00:13 - Broken Product Media
- **Problem**: User suspected broken image links in `products.json`.
- **Investigation**: Created `verify_images.py` to audit all 50 URLs.
- **Result**: Identified 9 broken Unsplash links (404 Not Found).
- **Solution**: Replaced all 9 URLs with fresh, high-quality Unsplash images verified to return `200 OK`.

### 00:46 - Backend Import Error
- **Problem**: `ImportError: attempted relative import with no known parent package` when running `python main.py`.
- **Cause**: Python does not support relative imports (e.g., `from .ml_service`) when a script is executed directly as the main module.
- **Solution**: Converted relative imports in `backend/main.py` and `backend/database.py` to absolute imports (e.g., `from ml_service`).

### 01:03 - Search 500 Error / Blank Results
- **Problem**: Frontend displayed `"Failed to find similar products"` every time.
- **Cause 1 (Data)**: The `products_with_embeddings.json` file contained `null` values because Unsplash was blocking the precompute script (bot protection).
- **Cause 2 (Logic)**: The backend crashed when performing cosine similarity on `null` vectors.
- **Solution**: 
  - Added a `User-Agent` header to image requests in `ml_service.py`.
  - Added a defensive check in `database.py` to filter out products with missing embeddings.

### 01:08 - AI Model Runtime Error (AttributeError)
- **Problem**: `Failed to process: 'BaseModelOutputWithPooling' object has no attribute 'norm'`.
- **Cause**: Newer versions of the Hugging Face `transformers` library return a `BaseModelOutput` object instead of a raw tensor when calling `get_image_features`.
- **Solution**: Updated `ml_service.py` to explicitly check for the object type and extract the `.image_embeds` attribute before normalization.

### 01:31 - AI Model Input Error (ValueError)
- **Problem**: `Failed to process: You have to specify input_ids`.
- **Cause**: Attempting to use the direct model forward call `self.model(...)` which defaults to requiring both vision and text inputs.
- **Solution**: Reverted to using `self.model.get_image_features()` but kept the robust tensor extraction logic to handle both raw tensors and output objects.

### 02:09 - Tensor Dimensionality Error (ValueError)
- **Problem**: `ValueError: Found array with dim 3, while dim <= 2 is required`.
- **Cause**: Some versions of CLIP/Transformers return nested tensors (e.g., shape `[1, 1, 512]`), causing embeddings to be saved as nested lists.
- **Solution**: Added `.flatten()` to both the ML service (before saving) and the Database service (during search) to ensure all vectors are standardized to 1D arrays.

## 🏁 Final Status: 01:51
- **Status**: 100% Resolved.
- **Verification**: `python verify_images.py` and `python precompute.py` both passed with 50/50 success.
