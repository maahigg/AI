import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
import numpy as np
import requests
from transformers import BlipProcessor, BlipForConditionalGeneration
import torch

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

UCLASSIFY_READ_API_KEY ="2SA6uoG0hDtK"
UCLASSIFY_SENTIMENT_URL = "https://api.uclassify.com/v1/uClassify/Sentiment/classify"

def generate_caption(image_path):
    raw_image = Image.open(image_path).convert('RGB')
    inputs = processor(raw_image, return_tensors = "pt")
    out = model.generate(**inputs)
    caption=processor.decode(out[0], skip_special_tokens=True)
    return caption

def classify_text(text):
    headers = {
        "Authorization": f"Token {UCLASSIFY_READ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {"texts": [text]}
    response = requests.post(UCLASSIFY_SENTIMENT_URL, headers=headers, json=data)
    result = response.json()
    sentiment = result[0]['classification']
    return sentiment

def inpaint_image(img_path, mask_path):
    img = cv2.imread(img_path)
    mask = cv2.imread(mask_path, 0)
    restored = cv2.inpaint(img, mask, 3, cv2.INPAINT_TELEA)
    restored_path = "restored.jpg"
    cv2.imwrite(restored_path, restored)
    return restored_path

class CaptionCureApp:
    def __init__(self, root):
        self.root = root
        self.root.title("caption cure")
        self.canvas = tk.Canvas(root, width=400, height=300)
        self.canvas.pack()

        self.upload_btn = tk.Button(root, text="upload image", command=self.upload_image)
        self.upload_btn.pack()

        self.caption_label = tk.Label(root, text="", wrapLength=380)
        self.caption_label.pack()

        self.sentiment_label = tk.Label(root, text="", wraplength=380)
        self.sentiment_label.pack()

    def upload_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            img=Image.open(file_path).resize((400, 300))
            self.tk_img = ImageTk.PhotoImage(img)
            self.canvas.create_image(0, 0, anchor="nw", image=self.tk_img)

            caption = generate_caption(file_path)
            self.caption_label.config(text=f"caption: {caption}")

            sentiment = classify_text(caption)
            sentiment_str = ", ".join([f"{s['className']}: {s['p']:.2f}" for s in sentiment])
            self.sentiment_label.config(text=f"sentiment: {sentiment_str}")

root = tk.Tk()
app = CaptionCureApp(root)
root.mainloop()