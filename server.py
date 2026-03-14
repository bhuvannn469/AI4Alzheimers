# Build a FastAPI backend for MRI Alzheimer classification.
# Requirements:
# - Load a PyTorch ResNet50 model from ./models/best_model.pt
# - Model has 4 output classes:
#   0 = Non-Demented
#   1 = Very Mild Demented
#   2 = Mild Demented
#   3 = Moderate Demented
# - Accept an uploaded image via POST /predict (multipart/form-data)
# - Preprocess exactly like training:
#   resize to 224x224, convert to RGB, normalize with ImageNet mean/std
# - Return JSON:
#   { "predicted_class": "...", "probability": 0.0-1.0 list per class }
# - Enable CORS for http://localhost:3000
# - Keep the model loaded globally (do not reload each request)
# - Device CPU is fine for inference

import os
import io
import torch
import torch.nn as nn
from torchvision import models, transforms
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
from typing import List
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- CONFIGURATION ---
MODEL_PATH = "../models/best_model.pt"

# Class labels in order (0-3)
CLASS_NAMES = [
    "Non-Demented",           # 0
    "Very Mild Demented",     # 1
    "Mild Demented",          # 2
    "Moderate Demented"       # 3
]

# Initialize FastAPI app
app = FastAPI(
    title="Alzheimer's MRI Classification API",
    description="ResNet50-based classification for Alzheimer's disease stages",
    version="1.0.0"
)

# --- CORS Configuration ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # Vite default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Image Preprocessing Pipeline ---
# Matches ImageNet normalization (ResNet50 standard)
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

# --- Model Loading ---
def load_model() -> nn.Module:
    """
    Load ResNet50 model with custom final layer for 4 classes.
    Handles state_dict loading on CPU.
    """
    logger.info(f"Loading model from: {os.path.abspath(MODEL_PATH)}")
    
    device = torch.device("cpu")
    
    # Initialize ResNet50 architecture
    model = models.resnet50(pretrained=False)
    
    # Replace final fully connected layer
    num_features = model.fc.in_features
    model.fc = nn.Linear(num_features, len(CLASS_NAMES))
    
    try:
        # Load trained weights
        state_dict = torch.load(MODEL_PATH, map_location=device)
        
        # Handle different save formats
        if isinstance(state_dict, dict):
            if 'state_dict' in state_dict:
                model.load_state_dict(state_dict['state_dict'])
            elif 'model_state_dict' in state_dict:
                model.load_state_dict(state_dict['model_state_dict'])
            else:
                model.load_state_dict(state_dict)
        else:
            # Assume it's the model itself
            model = state_dict
        
        model.eval()  # Set to evaluation mode
        model.to(device)
        
        logger.info("✓ Model loaded successfully")
        return model
        
    except FileNotFoundError:
        logger.error(f"Model file not found at: {MODEL_PATH}")
        raise
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        raise

# Global model instance (loaded once at startup)
try:
    model = load_model()
except Exception as e:
    logger.error("Failed to load model on startup")
    model = None

# --- API Endpoints ---

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "model_loaded": model is not None,
        "classes": CLASS_NAMES
    }

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    """
    Classify an uploaded MRI image.
    
    Args:
        file: Uploaded image file (JPG, PNG, etc.)
    
    Returns:
        JSON with predicted class and probability distribution
    """
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    # Validate file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        # Read and preprocess image
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        
        # Apply transforms and add batch dimension
        input_tensor = transform(image).unsqueeze(0)
        
        # Run inference
        with torch.no_grad():
            outputs = model(input_tensor)
            probabilities = torch.nn.functional.softmax(outputs, dim=1)
            
            # Get prediction
            confidence, predicted_idx = torch.max(probabilities, 1)
            predicted_class = CLASS_NAMES[predicted_idx.item()]
            
            # Convert probabilities to list
            prob_list = probabilities[0].tolist()
        
        logger.info(f"Prediction: {predicted_class} ({confidence.item():.2%})")
        
        return {
            "predicted_class": predicted_class,
            "probability": prob_list,
            "confidence": float(confidence.item()),
            "all_classes": CLASS_NAMES
        }
    
    except Exception as e:
        logger.error(f"Error during prediction: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/classes")
async def get_classes():
    """Return the list of classification classes"""
    return {"classes": CLASS_NAMES}

# --- Run Server ---
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )