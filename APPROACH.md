# Project Approach: Visual Product Matcher

For this assessment, I built a visual search engine that leverages semantic image understanding rather than simple pixel matching.

### Core Technology: CLIP
I chose **OpenAI’s CLIP (ViT-B/32)** model because it maps images and text into a shared latent space. This allows the system to understand "product concepts" (e.g., a "modern sofa" vs. a "rustic chair") based on visual features rather than just color histograms.

### Architecture & Efficiency
1.  **Offline Precomputation**: To ensure sub-second search times, I precompute 512-dimension embeddings for the 50+ catalog items. These are stored as numerical vectors.
2.  **In-Memory Search**: Since the catalog is small (50 items), I use **Cosine Similarity** on in-memory NumPy arrays. For larger scales, I would transition to a vector database like FAISS or Milvus.
3.  **FastAPI Backend**: Provides a lightweight API with asynchronous file handling for image uploads.
4.  **React Frontend**: Built with a "premium" aesthetic using glassmorphism and real-time similarity filtering to give the user immediate feedback.

### Trade-offs & Improvements
To prioritize speed and demo-readiness, I used an in-memory database. Future improvements would include robust image caching and a dedicated vector search service.
