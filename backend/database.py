import json
import os
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def find_data_file(filename):
    # Try current dir/data/filename (for Docker structure)
    path1 = os.path.join(os.path.dirname(__file__), "data", filename)
    # Try parent dir/data/filename (for local structure where database.py is in backend/)
    path2 = os.path.join(os.path.dirname(__file__), "..", "data", filename)
    
    if os.path.exists(path1):
        return path1
    return path2

DATA_PATH = find_data_file("products.json")
EMBEDDINGS_PATH = find_data_file("products_with_embeddings.json")

class ProductDatabase:
    def __init__(self):
        self.products = []
        self.load_data()

    def load_data(self):
        # Prefer embeddings file if it exists
        path = EMBEDDINGS_PATH if os.path.exists(EMBEDDINGS_PATH) else DATA_PATH
        if os.path.exists(path):
            with open(path, "r") as f:
                self.products = json.load(f)
        else:
            self.products = []

    def get_all_products(self):
        return self.products

    def search_similar(self, query_embedding, top_k=10):
        # Filter out products that don't have a valid embedding
        valid_products = [p for p in self.products if p.get("embedding") is not None]
        
        if not valid_products:
            return []

        # Convert to numpy and ensure all vectors are 1D (flattened)
        # This handles cases where embeddings might have been saved as nested lists
        product_embeddings = np.array([np.array(p["embedding"]).flatten() for p in valid_products])
        query_embedding = np.array(query_embedding).flatten().reshape(1, -1)

        similarities = cosine_similarity(query_embedding, product_embeddings)[0]
        
        # Add similarity scores to products
        results = []
        for i, product in enumerate(valid_products):
            # Copy product to avoid modifying original
            p_copy = product.copy()
            p_copy["similarity"] = float(similarities[i])
            # Remove embedding from response to save bandwidth
            if "embedding" in p_copy:
                del p_copy["embedding"]
            results.append(p_copy)

        # Sort by similarity
        results.sort(key=lambda x: x["similarity"], reverse=True)
        return results[:top_k]

db = ProductDatabase()

def get_db():
    return db
