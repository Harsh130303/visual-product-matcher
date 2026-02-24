import torch
from PIL import Image
import requests
from io import BytesIO
from transformers import CLIPProcessor, CLIPModel

class MLService:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model_name = "openai/clip-vit-base-patch32"
        self.model = CLIPModel.from_pretrained(self.model_name).to(self.device)
        self.processor = CLIPProcessor.from_pretrained(self.model_name)

    def get_image_embedding(self, image_input):
        """
        Generates an embedding for an image (URL or PIL Image).
        """
        if isinstance(image_input, str):
            # Use headers to avoid being blocked by some sites
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
            response = requests.get(image_input, headers=headers)
            image = Image.open(BytesIO(response.content)).convert("RGB")
        else:
            image = image_input.convert("RGB")

        inputs = self.processor(images=image, return_tensors="pt").to(self.device)
        with torch.no_grad():
            # Use get_image_features which is specifically for vision-only embeddings
            outputs = self.model.get_image_features(pixel_values=inputs.pixel_values)
            
        # Ensure we have the raw tensor
        if hasattr(outputs, "last_hidden_state") or not isinstance(outputs, torch.Tensor):
            # If it's a dictionary-like object, try to get image_embeds or use indexing
            image_features = getattr(outputs, "image_embeds", outputs if isinstance(outputs, torch.Tensor) else outputs[0])
        else:
            image_features = outputs

        # Final check to ensure we have a tensor
        if not isinstance(image_features, torch.Tensor):
             image_features = torch.tensor(image_features)

        # Normalize the features
        image_features = image_features / image_features.norm(p=2, dim=-1, keepdim=True)
        
        # Flatten to a 1D list for storage/consistency
        embedding = image_features.cpu().numpy().flatten().tolist()
        return embedding

# Singleton instance
ml_service = None

def get_ml_service():
    global ml_service
    if ml_service is None:
        ml_service = MLService()
    return ml_service
