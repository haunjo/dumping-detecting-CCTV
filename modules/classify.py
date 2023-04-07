import os
import torch
from clip import clip
from PIL import Image

class Classifier():
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model, self.preprocess = clip.load("ViT-B/32", device=self.device)
        
        self.labels = [
            'dumping trash',
            'walking',
            'smoking',
            'sitting',
        ]
        
        self.text = [f"a photo of a person {label}" for label in self.labels]
        self.tokens = clip.tokenize(self.text).to(self.device)

    def classify(self, source):
        image = self.preprocess(Image.open(source)).unsqueeze(0).to(self.device)

        with torch.no_grad():
            image_features = self.model.encode_image(image)
            text_features = self.model.encode_text(self.tokens)

            logits_per_image, logits_per_text = self.model(image, self.tokens)
            probs = logits_per_image.softmax(dim=-1)

        pred = self.text[torch.argmax(probs)] # text of image's class
        
        if pred != 'a photo of a person dumping trash':
            try:
                os.remove(source)
                print("the image is removed.")
            except FileNotFoundError as e:
                print(e)