import cv2
import torch
from transformers import AutoImageProcessor, SiglipForImageClassification
from PIL import Image

# Load model
model_name = "prithivMLmods/Alphabet-Sign-Language-Detection"
model = SiglipForImageClassification.from_pretrained(model_name)
processor = AutoImageProcessor.from_pretrained(model_name)

labels = {i: chr(65+i) for i in range(26)}

def predict(frame):
    image = Image.fromarray(frame).convert("RGB")
    inputs = processor(images=image, return_tensors="pt")
    
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        probs = torch.nn.functional.softmax(logits, dim=1)
    
    pred_index = probs.argmax().item()
    confidence = probs.max().item()
    
    return labels[pred_index], confidence

# Open webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Flip for mirror effect
    frame = cv2.flip(frame, 1)

    # Resize for faster prediction
    small_frame = cv2.resize(frame, (224, 224))

    # Predict
    label, conf = predict(small_frame)

    # Show result on screen
    text = f"{label} ({conf:.2f})"
    cv2.putText(frame, text, (20, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1, (0, 255, 0), 2)

    cv2.imshow("Sign Language Detector", frame)

    # Press Q to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()