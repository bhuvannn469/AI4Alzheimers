# AI4Alzheimers - Setup Guide

Complete setup instructions for running the MRI Alzheimer's classification system.

## 📋 Prerequisites

- Python 3.9 or higher
- Node.js 16+ and npm
- PyTorch model file: `../models/best_model.pt`

## 🔧 Backend Setup (FastAPI)

### 1. Install Python Dependencies

```bash
cd alzheimers-app
pip install -r requirements.txt
```

Or install manually:

```bash
pip install fastapi uvicorn torch torchvision pillow python-multipart
```

### 2. Verify Model Path

Ensure your trained model is located at:

```
alzheimers/
  ├── models/
  │   └── best_model.pt  ← Your trained ResNet50 model
  └── alzheimers-app/
      └── server.py
```

The server expects the model at `../models/best_model.pt` relative to the `alzheimers-app` directory.

### 3. Start the Backend Server

```bash
cd alzheimers-app
uvicorn server:app --reload --port 8000
```

The API will be available at: `http://localhost:8000`

**API Endpoints:**

- `GET /` - Health check
- `POST /predict` - Upload image for classification
- `GET /classes` - Get list of classification classes

## ⚛️ Frontend Setup (React + Vite)

### 1. Install Dependencies

```bash
cd alzheimers-app
npm install
```

### 2. Start Development Server

```bash
npm run dev
```

The app will open at: `http://localhost:5173` (or `http://localhost:3000` depending on your Vite config)

## 🚀 Running the Complete System

### Option 1: Two Terminal Windows

**Terminal 1 - Backend:**

```bash
cd alzheimers-app
uvicorn server:app --reload --port 8000
```

**Terminal 2 - Frontend:**

```bash
cd alzheimers-app
npm run dev
```

### Option 2: Production Mode

**Backend (production):**

```bash
uvicorn server:app --host 0.0.0.0 --port 8000
```

**Frontend (build and serve):**

```bash
npm run build
npm run preview
```

## 🧪 Testing the API

### Using cURL

```bash
# Health check
curl http://localhost:8000/

# Predict with image
curl -X POST "http://localhost:8000/predict" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@path/to/mri_image.jpg"
```

### Using the Web Interface

1. Open `http://localhost:5173` in your browser
2. Upload an MRI scan image (JPG, PNG)
3. Click "Run Diagnosis"
4. View the classification results and probability distribution

## 📊 Expected Response Format

```json
{
  "predicted_class": "Non-Demented",
  "probability": [0.85, 0.08, 0.05, 0.02],
  "confidence": 0.85,
  "all_classes": [
    "Non-Demented",
    "Very Mild Demented",
    "Mild Demented",
    "Moderate Demented"
  ]
}
```

## 🔍 Model Specifications

- **Architecture:** ResNet50 (pretrained on ImageNet)
- **Input Size:** 224×224 RGB images
- **Normalization:** ImageNet mean/std
  - Mean: [0.485, 0.456, 0.406]
  - Std: [0.229, 0.224, 0.225]
- **Output Classes:** 4 (Non-Demented, Very Mild, Mild, Moderate)
- **Device:** CPU (for inference)

## ⚠️ Troubleshooting

### Backend Issues

**Problem:** Model file not found

```
Solution: Verify the path in server.py line 33:
MODEL_PATH = "../models/best_model.pt"
```

**Problem:** CUDA out of memory

```
Solution: The server uses CPU by default. No GPU needed.
```

**Problem:** Import errors

```bash
Solution: Reinstall dependencies:
pip install --upgrade -r requirements.txt
```

### Frontend Issues

**Problem:** Cannot connect to backend

```
Solution:
1. Verify backend is running on port 8000
2. Check CORS configuration in server.py
3. Update API_URL in App.jsx if needed
```

**Problem:** Image not displaying

```
Solution: Check browser console for errors
Ensure uploaded file is a valid image format
```

### CORS Issues

If you see CORS errors, verify the backend allows your frontend origin:

```python
# In server.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    ...
)
```

## 📝 Development Notes

### Backend (server.py)

- FastAPI with async support
- Global model loading (once at startup)
- Automatic image preprocessing pipeline
- Comprehensive error handling

### Frontend (App.jsx)

- React 18+ with hooks
- TailwindCSS for styling
- Drag-and-drop file upload
- Real-time probability visualization
- Loading states and error handling

## 🎯 Next Steps

- [ ] Add Grad-CAM visualization endpoint
- [ ] Implement batch prediction
- [ ] Add authentication
- [ ] Deploy to cloud (AWS/Azure)
- [ ] Add model performance metrics

## 📄 License

Educational and research purposes only.
