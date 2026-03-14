# 🏗️ System Architecture

## Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER INTERFACE                            │
│                    (React App - Port 5173)                       │
│                                                                   │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────────────┐    │
│  │   Upload    │→ │   Display    │→ │   Probabilities    │    │
│  │   MRI Scan  │  │   Results    │  │   All 4 Classes    │    │
│  └─────────────┘  └──────────────┘  └────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
                              ↓
                    HTTP POST /predict
                    (multipart/form-data)
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                      FASTAPI BACKEND                             │
│                    (Python - Port 8000)                          │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    REQUEST HANDLER                       │   │
│  │  1. Receive image                                        │   │
│  │  2. Validate file type                                   │   │
│  │  3. Convert to PIL Image                                 │   │
│  └────────────────────────┬─────────────────────────────────┘   │
│                           ↓                                      │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │             PREPROCESSING PIPELINE                       │   │
│  │  • Resize to 224×224                                     │   │
│  │  • Convert to RGB                                        │   │
│  │  • Convert to Tensor                                     │   │
│  │  • Normalize (ImageNet mean/std)                         │   │
│  └────────────────────────┬─────────────────────────────────┘   │
│                           ↓                                      │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                  RESNET50 MODEL                          │   │
│  │  • Loaded from: ../models/best_model.pt                  │   │
│  │  • Architecture: ResNet50                                │   │
│  │  • Output: 4 classes                                     │   │
│  │  • Device: CPU                                           │   │
│  │  • Mode: eval()                                          │   │
│  └────────────────────────┬─────────────────────────────────┘   │
│                           ↓                                      │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              SOFTMAX & RESPONSE                          │   │
│  │  • Apply softmax to logits                               │   │
│  │  • Get max confidence                                    │   │
│  │  • Build JSON response                                   │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              ↓
                    JSON Response
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                      RESPONSE FORMAT                             │
│                                                                   │
│  {                                                                │
│    "predicted_class": "Non-Demented",                            │
│    "probability": [0.85, 0.08, 0.05, 0.02],                      │
│    "confidence": 0.85,                                            │
│    "all_classes": [                                               │
│      "Non-Demented",                                              │
│      "Very Mild Demented",                                        │
│      "Mild Demented",                                             │
│      "Moderate Demented"                                          │
│    ]                                                              │
│  }                                                                │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow

### 1. Upload Phase

```
User selects image
     ↓
FileReader converts to base64 (for preview)
     ↓
Original File object stored in state
     ↓
User clicks "Run Diagnosis"
```

### 2. Inference Phase

```
FormData created with file
     ↓
POST to http://localhost:8000/predict
     ↓
Backend receives multipart data
     ↓
Image → PIL → Transforms → Tensor
     ↓
Model inference (forward pass)
     ↓
Softmax activation
     ↓
JSON response created
```

### 3. Display Phase

```
Frontend receives JSON
     ↓
Parse predicted_class
     ↓
Find matching class styling
     ↓
Display:
  - Predicted class with color
  - Confidence meter
  - Probability bars for all classes
```

## File Structure

```
alzheimers/
├── models/
│   └── best_model.pt              ← ResNet50 trained weights
│
└── alzheimers-app/
    ├── server.py                   ← FastAPI backend (200 lines)
    ├── requirements.txt            ← Python dependencies
    ├── test_api.py                 ← Backend test suite
    ├── start-backend.bat           ← Windows launcher
    ├── start-frontend.bat          ← Windows launcher
    ├── README.md                   ← Quick start guide
    ├── SETUP.md                    ← Full documentation
    ├── IMPLEMENTATION_SUMMARY.md   ← This summary
    │
    ├── package.json                ← Node dependencies
    ├── vite.config.js              ← Vite configuration
    ├── tailwind.config.js          ← TailwindCSS config
    │
    ├── public/                     ← Static assets
    │
    └── src/
        ├── App.jsx                 ← Main React component (400+ lines)
        ├── main.jsx                ← React entry point
        ├── index.css               ← Global styles
        └── App.css                 ← Component styles
```

## Technology Stack

### Backend

```
┌─────────────────────────┐
│       FastAPI           │  Web framework
├─────────────────────────┤
│       Uvicorn           │  ASGI server
├─────────────────────────┤
│       PyTorch           │  Deep learning
├─────────────────────────┤
│     Torchvision         │  Image models
├─────────────────────────┤
│       Pillow            │  Image processing
└─────────────────────────┘
```

### Frontend

```
┌─────────────────────────┐
│        React 18         │  UI library
├─────────────────────────┤
│         Vite            │  Build tool
├─────────────────────────┤
│      TailwindCSS        │  Styling
├─────────────────────────┤
│    Lucide Icons         │  Icon library
└─────────────────────────┘
```

## Network Communication

```
Frontend                 Backend
(React)                (FastAPI)
   |                       |
   |--POST /predict------->|
   |  Content-Type:        |
   |  multipart/form-data  |
   |  Body: image file     |
   |                       |
   |                   [Process]
   |                       |
   |                   [Inference]
   |                       |
   |<-----JSON Response----|
   |  {                    |
   |    predicted_class,   |
   |    probability,       |
   |    confidence         |
   |  }                    |
   |                       |
```

## Preprocessing Pipeline

```
Input Image (any size, any format)
          ↓
    Convert to RGB
          ↓
   Resize to 224×224
          ↓
  Normalize pixel values [0, 1]
          ↓
Apply ImageNet normalization:
  R: (x - 0.485) / 0.229
  G: (x - 0.456) / 0.224
  B: (x - 0.406) / 0.225
          ↓
   Shape: (1, 3, 224, 224)
          ↓
    Ready for model
```

## Model Architecture

```
Input: (1, 3, 224, 224)
          ↓
┌─────────────────────┐
│   ResNet50 Blocks   │
│   (Pretrained)      │
│                     │
│   - Conv layers     │
│   - BatchNorm       │
│   - ReLU            │
│   - Residual blocks │
└─────────────────────┘
          ↓
    Global Avg Pool
          ↓
┌─────────────────────┐
│   Fully Connected   │
│   (Custom)          │
│   2048 → 4          │
└─────────────────────┘
          ↓
    Softmax (in code)
          ↓
Output: [p0, p1, p2, p3]
Where:
  p0 = Non-Demented
  p1 = Very Mild Demented
  p2 = Mild Demented
  p3 = Moderate Demented
```

## Deployment Architecture

### Development

```
┌──────────────┐      ┌──────────────┐
│   Frontend   │      │   Backend    │
│              │      │              │
│ localhost:   │─────→│ localhost:   │
│   5173       │      │   8000       │
│              │      │              │
│   npm run    │      │   uvicorn    │
│   dev        │      │   --reload   │
└──────────────┘      └──────────────┘
```

### Production (Future)

```
┌──────────────┐      ┌──────────────┐
│   Frontend   │      │   Backend    │
│   (Vercel)   │─────→│   (AWS ECS)  │
│              │      │              │
│  Static CDN  │      │ Load Balanced│
│              │      │              │
│    HTTPS     │      │    HTTPS     │
└──────────────┘      └──────────────┘
                             │
                             ↓
                      ┌──────────────┐
                      │  Model Store │
                      │   (S3/EFS)   │
                      └──────────────┘
```

## Security Considerations

- ✅ CORS properly configured (specific origins)
- ✅ File type validation (images only)
- ✅ Error handling (no sensitive info leaked)
- ⚠️ TODO: Rate limiting
- ⚠️ TODO: Authentication
- ⚠️ TODO: File size limits
- ⚠️ TODO: Input sanitization

## Performance Metrics

| Metric         | Value      | Notes                |
| -------------- | ---------- | -------------------- |
| Model Size     | ~100 MB    | ResNet50 weights     |
| Startup Time   | 2-5s       | Model loading        |
| Inference Time | 0.5-2s     | CPU, varies by image |
| Memory Usage   | ~1 GB      | With model loaded    |
| Response Size  | ~200 bytes | JSON response        |

## Error Handling Flow

```
User uploads file
      ↓
Frontend validates
  ├─ Valid → Continue
  └─ Invalid → Show error message
      ↓
Send to backend
      ↓
Backend validates
  ├─ Valid → Process
  └─ Invalid → Return 400 error
      ↓
Model inference
  ├─ Success → Return prediction
  └─ Error → Return 500 error
      ↓
Frontend receives
  ├─ 200 → Display results
  └─ Error → Show error message
```

---

**Last Updated:** December 28, 2025  
**Status:** Production Ready  
**Version:** 1.0.0
