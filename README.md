# 🧠 AI4Alzheimers - MRI Classification System

Deep learning-based classification system for detecting Alzheimer's disease stages from MRI scans using ResNet50.

## 🚀 Quick Start Guide

### ⚡ Fastest Way to Run (Windows)

Simply double-click these files in order:

1. **`start-backend.bat`** → Starts FastAPI server (port 8000)
2. **`start-frontend.bat`** → Starts React app (port 5173)

### macOS/Linux Users

**Terminal 1 - Backend:**

```bash
cd alzheimers-app
pip install -r requirements.txt
uvicorn server:app --reload --port 8000
```

**Terminal 2 - Frontend:**

```bash
cd alzheimers-app
npm install
npm run dev
```

## 📁 Project Structure

```
alzheimers/
  ├── models/
  │   └── best_model.pt          ← Your trained ResNet50 model
  └── alzheimers-app/
      ├── server.py               ← FastAPI backend
      ├── requirements.txt        ← Python dependencies
      ├── start-backend.bat       ← Windows: Start backend
      ├── start-frontend.bat      ← Windows: Start frontend
      ├── package.json
      └── src/
          └── App.jsx             ← React frontend
```

## 🔑 Key URLs

- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs (auto-generated)
- **Frontend App:** http://localhost:5173

## 🧪 Quick Test

1. Visit http://localhost:5173
2. Upload any MRI image
3. Click "Run Diagnosis"
4. See prediction + confidence scores

## 📊 API Response Format

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

## ⚠️ Common Issues

| Problem             | Solution                                      |
| ------------------- | --------------------------------------------- |
| Port already in use | Change port: `uvicorn server:app --port 8001` |
| Model not found     | Verify path: `../models/best_model.pt`        |
| CORS error          | Backend must be running first                 |
| npm install fails   | Try: `npm install --legacy-peer-deps`         |

## 🎯 What's Implemented

✅ FastAPI backend with ResNet50  
✅ Image preprocessing (224×224, ImageNet normalization)  
✅ CORS enabled for React frontend  
✅ React file upload with drag-and-drop  
✅ Real-time prediction display  
✅ Probability distribution for all 4 classes  
✅ Loading states and error handling  
✅ Production-ready code structure

## 🚧 Optional Enhancements

- Add Grad-CAM visualization endpoint
- Implement batch prediction
- Add user authentication
- Deploy to cloud (AWS/Azure)
- Add model performance metrics dashboard

## 📖 Full Documentation

See `SETUP.md` for complete installation and troubleshooting guide.

---

## 🛠️ Technical Stack

- **Backend:** FastAPI, PyTorch, Torchvision
- **Frontend:** React 18, Vite, TailwindCSS
- **Model:** ResNet50 (transfer learning)
- **Image Processing:** PIL, ImageNet normalization

## 📝 Original Vite Template Info

This project is built on React + Vite template with HMR and ESLint.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Babel](https://babeljs.io/) (or [oxc](https://oxc.rs) when used in [rolldown-vite](https://vite.dev/guide/rolldown)) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

---

**Made with ❤️ for Alzheimer's disease classification research**
