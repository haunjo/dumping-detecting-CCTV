import os
import torch
from clip import clip
from PIL import Image

device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

def classify(image_path):
    image = preprocess(Image.open(image_path)).unsqueeze(0).to(device)
    labels = [
        'dupming trash',
        'walking',
        'smoking',
        'sitting',
    ]
    
    text = [f"a photo of a person {label}" for label in labels]
    tokens = clip.tokenize(text).to(device)

    with torch.no_grad():
        image_features = model.encode_image(image)
        text_features = model.encode_text(tokens)

        logits_per_image, logits_per_text = model(image, tokens)
        probs = logits_per_image.softmax(dim=-1)

    pred = text[torch.argmax(probs)] # text of image's class
    
    if pred != 'a photo of a person dumping trash':
        try:
            os.remove(image_path)
            print("the image is removed.")
        except FileNotFoundError as e:
            print(e)