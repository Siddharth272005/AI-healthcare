import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import AutoTokenizer, AutoModel
from PIL import Image
import torchvision.transforms as transforms
import torch

# Initializing Flask app
app = Flask(__name__)
CORS(app)

# Load the ClinicalBERT model for text
tokenizer = AutoTokenizer.from_pretrained("emilyalsentzer/Bio_ClinicalBERT")
model_text = AutoModel.from_pretrained("emilyalsentzer/Bio_ClinicalBERT")

# Define image transformation
image_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

# Load knowledge base
with open("knowledge_base.json", "r") as kb_file:
    knowledge_base = json.load(kb_file)["symptoms"]

@app.route("/predict", methods=["POST"])
def predict():
    try:
        result = {}
        user_input = request.form.get("text", "").lower()

        # Process text input
        if user_input:
            inputs = tokenizer(user_input, return_tensors="pt")
            with torch.no_grad():
                outputs = model_text(**inputs)
                text_embeddings = outputs.last_hidden_state.mean(dim=1).tolist()

            # Match input to knowledge base
            suggestion = "No match found in knowledge base."
            for symptom, advice in knowledge_base.items():
                if symptom in user_input:
                    suggestion = advice
                    break

            result["text_analysis"] = "Processed text input successfully."
            result["suggestion"] = suggestion

        # Handle image input (if provided)
        if "image" in request.files:
            image = request.files["image"]
            img = Image.open(image).convert("RGB")
            img_tensor = image_transform(img).unsqueeze(0)

            # Dummy image analysis logic (can be extended)
            result["image_analysis"] = "Image processed successfully, but no specific logic implemented yet."

        return jsonify(suggestion)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)