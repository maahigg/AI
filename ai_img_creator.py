import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import requests
from transformers import BlipProcessor, BlipForConditionalGeneration
import torch

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

UCLASSIFY_API_KEY = "2SA6uoG0hDtK"
CLASSIFIER_NAME = "Topics"

def generate_caption(image_path):
    raw_image = Image.open(image_path).convert('RGB')
    inputs = processor(raw_image, return_tensors = "pt")
    out = model.generate(**inputs)
    caption=processor.decode(out[0], skip_special_tokens=True)
    return caption

def classify_caption(caption):
    url = f"https//api.uclassify.com/v1/uClassify/{CLASSIFIER_NAME}/classify"
    headers = {
        'Authorization': f'Token {UCLASSIFY_API_KEY}',
        'Content-Type': 'application/json'
    }

    data = {"texts":[caption]}
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        results = response.json()['classification']
        top = sorted(results[0]['classification'], key=lambda x: x['p'], reverse=True)[:3]
        return [(c['className'], round(c['p'], 2)) for c in top]
    else:
        return [("Error", 0)]

class CaptionClassifierApp:
    def __init__(self, root):
        self.root = root
        self.root.title("image caption + uClassify")
        self.root.geometry("600x500")

        self.label = tk.Label(root, text="upload an image to caption and classify", font =("Arial", 14))
        self.label.pack(pady=10)

        self.canvas = tk.Canvas(root, width=400, height=300)
        self.canvas.pack()

        tk.Button(root, text="upload image", command=self.upload_image).pack(pady=10)
        tk.Label(root, textvariable=self.caption_text, wraplength=500, font=("Arial", 12)).pack(pady=5)
        tk.Label(root, textvariable=self.classify_text, wraplength=500, font=("Arial", 12)).pack(pady=5)
    
    def upload_image(self):
        file_path = filedialog.askopenfilename()
        if not file_path:
            return
        
        try:
            img = Image.open(file_path)
            img.thumbnail((400, 300))
            self.tk_img = ImageTk.PhotoImage(img)
            self.canvas.create_image(200, 150, image=self.tk_img)

            caption = generate_caption(file_path)
            self.caption_text.set("caption: {caption}")

            classification = classify_caption(caption)
            result_str = "classification:\n" + "\n".join([f"{c[0]} ({c[1]*100:.1f}%)" for c in classification])
            self.classify_text.set(result_str)
        
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = CaptionClassifierApp(root)
    root.mainloop()