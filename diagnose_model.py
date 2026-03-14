"""
Diagnostic script to understand why the model predicts Mild Demented for everything
"""

import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import numpy as np

print("=" * 80)
print("  🔍 Model Diagnostic Tool")
print("=" * 80)
print()

# Load model
print("Loading model...")
MODEL_PATH = "../models/best_model.pt"
device = torch.device("cpu")

model = models.resnet50(pretrained=False)
num_features = model.fc.in_features
model.fc = nn.Linear(num_features, 4)

state_dict = torch.load(MODEL_PATH, map_location=device)
model.load_state_dict(state_dict)
model.eval()

print("✅ Model loaded")
print()

# Check final layer weights
print("📊 Analyzing final layer (fc) weights...")
fc_weights = model.fc.weight.data
fc_bias = model.fc.bias.data

print(f"   Weight shape: {fc_weights.shape}")
print(f"   Bias values: {fc_bias.tolist()}")
print()

# Check if weights are reasonable
weight_norms = torch.norm(fc_weights, dim=1)
print(f"   Weight norms per class:")
for i, norm in enumerate(weight_norms):
    class_names = ["Non-Demented", "Very Mild", "Mild", "Moderate"]
    print(f"      Class {i} ({class_names[i]:15s}): {norm:.4f}")
print()

# Check bias
print(f"   Bias analysis:")
for i, bias in enumerate(fc_bias):
    class_names = ["Non-Demented", "Very Mild", "Mild", "Moderate"]
    print(f"      Class {i} ({class_names[i]:15s}): {bias:.4f}")
print()

# Test with random inputs to see what model predicts
print("🎲 Testing with 10 random images...")
print()

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

class_counts = [0, 0, 0, 0]

for i in range(10):
    # Create random image
    random_img = Image.fromarray(np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8))
    input_tensor = transform(random_img).unsqueeze(0)
    
    with torch.no_grad():
        outputs = model(input_tensor)
        probabilities = torch.nn.functional.softmax(outputs, dim=1)
        predicted_idx = torch.argmax(probabilities).item()
        class_counts[predicted_idx] += 1
        
        print(f"   Test {i+1}: Predicted class {predicted_idx}, Probs: {probabilities[0].tolist()}")

print()
print("📈 Prediction distribution across 10 random images:")
class_names = ["Non-Demented", "Very Mild", "Mild", "Moderate"]
for i, count in enumerate(class_counts):
    bar = "█" * count
    print(f"   {class_names[i]:15s}: {count}/10 {bar}")
print()

if class_counts[2] == 10:
    print("⚠️  PROBLEM IDENTIFIED: Model ALWAYS predicts Mild Demented!")
    print()
    print("This means your model has one of these issues:")
    print("  1. Severe class imbalance in training data")
    print("  2. Model not properly trained/converged")
    print("  3. Final layer weights are stuck/frozen")
    print("  4. Training data had mostly Mild Demented samples")
    print()
    print("💡 SOLUTIONS:")
    print("  1. Retrain the model with balanced class weights")
    print("  2. Use class_weight parameter in loss function")
    print("  3. Apply data augmentation to minority classes")
    print("  4. Check your training data distribution")
    print("  5. Train for more epochs with lower learning rate")
elif max(class_counts) >= 8:
    print(f"⚠️  PROBLEM: Model has strong bias toward class {class_counts.index(max(class_counts))}")
    print("   The model may have been trained on imbalanced data.")
else:
    print("✅ Model seems to make varied predictions")
    print("   The issue might be with specific input images")

print()
print("=" * 80)
