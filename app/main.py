from fastapi import FastAPI, File, UploadFile, HTTPException
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import torch
import io
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Load model and processor
try:
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)
    logger.info("Model and processor loaded successfully")
except Exception as e:
    logger.error(f"Error loading model: {e}")
    raise

@app.post("/caption")
async def generate_caption(file: UploadFile = File(...)):
    try:
        # Validate file type
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="File must be an image")

        # Read and process image
        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data)).convert("RGB")
        
        # Prepare inputs
        inputs = processor(images=image, return_tensors="pt").to(device)
        
        # Generate caption
        outputs = model.generate(**inputs, max_length=50)
        caption = processor.decode(outputs[0], skip_special_tokens=True)
        
        logger.info(f"Generated caption: {caption}")
        return {"caption": caption}
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        raise HTTPException(status_code=500, detail=str(e))