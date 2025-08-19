import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import requests
import io
import base64

def generate_caption(image_path):
    return "A group of people hiking in the mountains"

def classify_text(text):
    api_key = "2SA6uoG0hDtK"
    url = "https://api.uclassify.com/v1/uClassify/Sentiment/classify"
    headers = {
        "Authorization": f"Token {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "texts": [text]
    }

    response = requests.post(url, headers=headers, json=data)
    result = response.json()
    return result[0]['classification']

def upload_image():
    file_path= filedialog.askopenfilename()
    if file_path:
        img = Image.open(file_path)
        img.thumbnail((300, 300))
        img_tk = ImageTk.PhotoImage(img)
        image_label.config(image=img_tk)
        image_label.image = img_tk

        caption = generate_caption(file_path)
        result = classify_text(caption)

        caption_label.config(text = f"caption: {caption}")
        result_label.config(text=f"classification: {result}")

root = tk.Tk()
root.title("image to text classifier")

tk.Button(root, text = "upload image", command=upload_image).pack()
image_label = tk.Label(root)
image_label.pack()

caption_label = tk.Label(root, text="Caption: ")
caption_label.pack()

result_label = tk.Label(root, text="classification: ")
result_label.pack()

root.mainloop()