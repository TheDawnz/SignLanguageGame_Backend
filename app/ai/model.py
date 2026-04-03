from transformers import AutoImageProcessor, SiglipForImageClassification
from PIL import Image
import torch

model_name = "prithivMLmods/Alphabet-Sign-Language-Detection"

model = SiglipForImageClassification.from_pretrained(model_name)
processor = AutoImageProcessor.from_pretrained(model_name)

labels = {str(i): chr(65+i) for i in range(26)}

def predict_sign(image_array):
    image = Image.fromarray(image_array).convert("RGB")
    inputs = processor(images=image, return_tensors="pt")
    
    with torch.no_grad():
        outputs = model(**inputs)
        probs = torch.nn.functional.softmax(outputs.logits, dim=1)
    
    predicted_index = probs.argmax().item()
    return labels[str(predicted_index)]