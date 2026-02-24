import json
import os
from ml_service import get_ml_service

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "products.json")
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "products_with_embeddings.json")

def precompute():
    print("Loading ML Service...")
    ml = get_ml_service()
    
    if not os.path.exists(DATA_PATH):
        print(f"Error: {DATA_PATH} not found.")
        return

    with open(DATA_PATH, "r") as f:
        products = json.load(f)

    print(f"Processing {len(products)} products...")
    for i, product in enumerate(products):
        print(f"[{i+1}/{len(products)}] Computing embedding for: {product['name']}")
        try:
            embedding = ml.get_image_embedding(product["image_url"])
            product["embedding"] = embedding
        except Exception as e:
            print(f"Failed to process {product['name']}: {e}")
            product["embedding"] = None

    # Filter out failed ones if necessary, or just save
    with open(OUTPUT_PATH, "w") as f:
        json.dump(products, f, indent=2)
    
    print(f"Precomputation complete. Saved to {OUTPUT_PATH}")

if __name__ == "__main__":
    precompute()
