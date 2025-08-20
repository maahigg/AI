import tkinter as tk
from tkinter import scrolledtext
from transformers import pipeline
import requests

summarizer = pipeline("summarization", model = "facebook/bart-large-cnn")
UCLASSIFY_API_KEY = "2SA6uoG0hDtK"
UCLASSIFY_URL = "https://api.uclassify.com/v1/uClassify/Topics/classify"

def summarize_text(text):
    summary = summarizer(text, max_length = 100, min_length = 30, do_sample = False)
    return summary[0]['summary_text']

def classify_summary(summary):
    headers = {
        "Authorization": f"Token {UCLASSIFY_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "texts": [summary]
    }

    response = requests.post(UCLASSIFY_URL, headers=headers, json = data)
    results = response.json()[0]['classification']
    return "\n".join([f"{item['className']}: {item['p']:.2f}" for item in results])

def process_text():
    input_text = text_input.get("1.0", tk.END).strip()
    if not input_text:
        output_summary.delete("1.0", tk.END)
        output_summary.insert(tk.END, "please enter some text.")
        return
    
    summary = summarize_text(input_text)
    classification = classify_summary(summary)

    output_summary.delete("1.0", tk.END)
    output_summary.insert(tk.END, f"summary:\n{summary}\n\nclassification:\n{classification}")

root = tk.Tk()
root.title("text summarizer classifier")

tk.Label(root, text="enter your text:").pack()
text_input = scrolledtext.ScrolledText(root, wrap = tk.WORD, width = 60, height=10)
text_input.pack(padx=10, pady=5)

tk.Button(root, text="summarize and classify", command=process_text).pack(pady=10)

output_summary = scrolledtext.ScrolledText(root, wrap = tk.WORD, width=60, height=15)
output_summary.pack(padx=10, pady=5)

root.mainloop()