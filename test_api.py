"""
Test script to verify the backend API is working correctly.
Run this after starting the backend server.
"""

import requests
import sys
from pathlib import Path

API_URL = "http://localhost:8000"

def test_health_check():
    """Test the root endpoint"""
    print("🧪 Testing health check endpoint...")
    try:
        response = requests.get(f"{API_URL}/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed!")
            print(f"   - Status: {data['status']}")
            print(f"   - Model loaded: {data['model_loaded']}")
            print(f"   - Classes: {data['classes']}")
            return True
        else:
            print(f"❌ Health check failed with status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to backend. Is the server running?")
        print("   Start it with: uvicorn server:app --reload --port 8000")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_classes_endpoint():
    """Test the /classes endpoint"""
    print("\n🧪 Testing classes endpoint...")
    try:
        response = requests.get(f"{API_URL}/classes")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Classes endpoint passed!")
            print(f"   - Available classes: {data['classes']}")
            return True
        else:
            print(f"❌ Classes endpoint failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_predict_endpoint():
    """Test the /predict endpoint with a dummy image"""
    print("\n🧪 Testing predict endpoint...")
    print("   Note: This requires an actual image file to test")
    
    # Look for any image file in common locations
    test_image_paths = [
        "../Datasets/MRI Dataset/Kaggle MRI Alzheimers",
        "test_image.jpg",
        "sample.png"
    ]
    
    test_image = None
    for path in test_image_paths:
        p = Path(path)
        if p.exists():
            if p.is_dir():
                # Find first image in directory
                for img_path in p.rglob("*.jpg"):
                    test_image = img_path
                    break
                if not test_image:
                    for img_path in p.rglob("*.png"):
                        test_image = img_path
                        break
            else:
                test_image = p
            if test_image:
                break
    
    if not test_image:
        print("⚠️  No test image found. Skipping predict endpoint test.")
        print("   To test this endpoint, upload an image through the web interface.")
        return None
    
    print(f"   Using test image: {test_image}")
    
    try:
        with open(test_image, 'rb') as f:
            files = {'file': f}
            response = requests.post(f"{API_URL}/predict", files=files)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Predict endpoint passed!")
            print(f"   - Predicted class: {data['predicted_class']}")
            print(f"   - Confidence: {data['confidence']:.2%}")
            print(f"   - Probabilities: {[f'{p:.2%}' for p in data['probability']]}")
            return True
        else:
            print(f"❌ Predict endpoint failed with status {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("=" * 60)
    print("  AI4Alzheimers Backend API Test Suite")
    print("=" * 60)
    
    results = []
    
    # Run tests
    results.append(test_health_check())
    if results[0]:  # Only continue if health check passed
        results.append(test_classes_endpoint())
        result = test_predict_endpoint()
        if result is not None:
            results.append(result)
    
    # Summary
    print("\n" + "=" * 60)
    passed = sum(1 for r in results if r is True)
    total = len(results)
    
    if passed == total:
        print(f"✅ All {total} tests passed!")
        print("\n🎉 Backend is working correctly!")
        print("   You can now use the web interface at http://localhost:5173")
        sys.exit(0)
    else:
        print(f"⚠️  {passed}/{total} tests passed")
        print("\nPlease check the errors above and ensure:")
        print("  1. Backend server is running (uvicorn server:app --reload --port 8000)")
        print("  2. Model file exists at ../models/best_model.pt")
        print("  3. All dependencies are installed (pip install -r requirements.txt)")
        sys.exit(1)

if __name__ == "__main__":
    main()
