from PIL import Image
import torch
import torch.nn as nn
import torchvision.transforms as transforms
from typing import Dict
import json
import os

class SkinLesionModel(nn.Module):
    def __init__(self):
        super().__init__()
        # Using ResNet18 as base model
        self.model = torch.hub.load('pytorch/vision:v0.10.0', 'resnet18', pretrained=True)
        # Modify last layer for binary classification
        self.model.fc = nn.Linear(512, 2)
        
    def forward(self, x):
        return self.model(x)

def analyze_medical_image(image_path: str) -> Dict:
    """
    Analyze skin lesion images for melanoma detection
    Using a locally stored model
    """
    try:
        # Load model and configurations
        model_path = os.path.join(os.path.dirname(__file__), 'medical_model', 'model.pth')
        config_path = os.path.join(os.path.dirname(__file__), 'medical_model', 'config.json')
        
        # Load configurations
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        # Initialize model
        model = SkinLesionModel()
        model.load_state_dict(torch.load(model_path))
        model.eval()
        
        # Image preprocessing
        transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                              std=[0.229, 0.224, 0.225])
        ])
        
        # Load and preprocess image
        image = Image.open(image_path)
        image = transform(image).unsqueeze(0)
        
        # Get prediction
        with torch.no_grad():
            outputs = model(image)
            probabilities = torch.nn.functional.softmax(outputs, dim=1)
            
        # Get predicted class and confidence
        predicted_class_id = probabilities.argmax().item()
        confidence = float(probabilities[0][predicted_class_id])
        
        id2label = {0: "Benign", 1: "Malignant"}
        result = id2label[predicted_class_id]
        
        return {
            "status": "success",
            "result": result,
            "confidence": f"{confidence:.2%}",
            "message": f"Analysis complete. The lesion appears to be {result.lower()} (Confidence: {confidence:.2%})",
            "details": {
                "benign_probability": f"{float(probabilities[0][0]):.2%}",
                "malignant_probability": f"{float(probabilities[0][1]):.2%}"
            }
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error analyzing image: {str(e)}"
        }

if __name__ == "__main__":
    # Test with a sample image
    test_image = "test.jpg"
    result = analyze_medical_image(test_image)
    print(result) 