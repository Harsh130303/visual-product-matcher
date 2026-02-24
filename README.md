# Visual Product Matcher
Deployed: 2026-02-24

A professional-grade web application that finds visually similar products from a curated catalog using OpenAI's CLIP (Contrastive Language-Image Pre-training) model.

## 🚀 Key Features
- **Visual Similarity Search**: Real-time vector matching using cosine similarity.
- **Multimodal Input**: Support for both local image uploads and remote image URLs.
- **Premium Design**: Modern, glassmorphism-inspired UI with smooth micro-animations.
- **Robust Backend**: FastAPI integration with optimized tensor processing and error handling.

## 📂 Project Structure
```text
.
├── backend/            # FastAPI server & ML logic
├── frontend/           # React (Vite) application
├── data/               # Product catalog & precomputed embeddings
└── README.md           # This documentation
```

## 🛠️ Tech Stack
- **Frontend**: React, Vite, Vanilla CSS.
- **Backend**: FastAPI (Python), Uvicorn.
- **ML Engine**: CLIP (openai/clip-vit-base-patch32) via Hugging Face Transformers.
- **Data Management**: In-memory vector search with NumPy and Scikit-learn.

## ⚡ Quick Start

### 1. Backend Setup
1. Navigate to `backend/`.
2. Install dependencies: `pip install -r requirements.txt`.
3. (Optional) Re-generate embeddings: `python precompute.py`.
4. Start server: `python main.py`.

### 2. Frontend Setup
1. Navigate to `frontend/`.
2. Install dependencies: `npm install`.
3. Start development server: `npm run dev`.
4. Open `http://localhost:5173` in your browser.

## 🛠️ Troubleshooting & Known Fixes
- **Import Errors**: The backend is configured for absolute imports. Always run scripts from the `backend/` directory.
- **AI Model Returns**: The code handles diverse tensor return types (BaseModelOutput vs. raw Tensors) across different library versions.
- **Dimensionality**: All embeddings are automatically flattened to 1D vectors to ensure compatibility with similarity engines.
- **User-Agent**: External image downloads are configured with valid headers to avoid bot protection blocks from sites like Unsplash.

## ✅ Submission Checklist Compliance
- [x] **No unnecessary files**: Excluded `node_modules`, `__pycache__`, and temp files via `.gitignore`.
- [x] **Minimal Dependencies**: Only used essential libraries for ML and Web APIs.
- [x] **Clean Architecture**: Decoupled ML service from the API and Database layers.
- [x] **Documentation**: Consolidated into this definitive README.
