from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
try:
    from ml_service import get_ml_service
    from database import get_db
except ImportError:
    from backend.ml_service import get_ml_service
    from backend.database import get_db
from PIL import Image
from io import BytesIO
import uvicorn

app = FastAPI(title="Visual Product Matcher API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/products")
def get_products():
    db = get_db()
    # Return products without embeddings
    products = []
    for p in db.get_all_products():
        p_copy = p.copy()
        if "embedding" in p_copy:
            del p_copy["embedding"]
        products.append(p_copy)
    return products

@app.post("/search")
async def search_products(
    file: UploadFile = File(None),
    image_url: str = Form(None)
):
    if not file and not image_url:
        raise HTTPException(status_code=400, detail="Either file or image_url must be provided")

    ml = get_ml_service()
    db = get_db()

    try:
        if file:
            contents = await file.read()
            image = Image.open(BytesIO(contents))
            query_embedding = ml.get_image_embedding(image)
        else:
            query_embedding = ml.get_image_embedding(image_url)

        results = db.search_similar(query_embedding)
        return {"results": results}
    except Exception as e:
        # Keep logging the traceback to the server logs
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Internal Server Error")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
