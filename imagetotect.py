import tkinter as tk 
from tkinter import filedialog
import requests
import pyttsx3
import matplotlib.pyplot as plt

UCLASSIFY_API_KEY = '2SA6uoG0hDtK'

def classify_text(text):
    headers = {"Authorization": f"Token {UCLASSIFY_API_KEY}"}
    data = {"texts": [text]}

    sentiment_res = requests.post(
        "https://api.uclassify.com/v1/uClassify/Sentiment/classify",
        json=data, headers=headers).json()
    
    topic_res = requests.post(
        "https://api.uclassify.com/v1/uClassify/topics/classify",
        json=data, headers=headers
    ).json()

    sentiment = sentiment_res['classification'][0]
    topics = topic_res['classification']
    return sentiment, topics

def generate_caption(option):
    if option == 1:
        return 'sunset over mountain peaks'
    elif option == 2:
        return 'a breathtaking sunset casting golden hues over rugged mountain peaks and tracks'
    elif option == 3:
        return ("the image captures a serene landscape where the sun sets behind majestic mountains creating a painting in the sky in warm tones and evoking a sense of peace and wonder")
    else:
        root.quit()

def speak_text(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.say(text)
    engine.runAndWait()

def show_bar_chart(classifications, title="topic probabilities"):
    labels = [c['className'] for c in classifications]
    scores = [c['p'] for c in classifications]

    plt.figure(figsize=(8, 4))
    plt.barh(labels, scores, color='skyblue')
    plt.xlabel("probability")
    plt.title(title)
    plt.tight_layout()
    plt.show()

def on_option_select(option):
    caption = generate_caption(option)
    sentiment, topics = classify_text(caption)

    sentiment_label = sentiment['className']
    top_topic = max(topics, key=lambda x: x['p'])['className']

    result_text = f"caption:/n{caption}/n/n sentiment is {sentiment_label}. topic is {top_topic}"
    result_label.config(text=result_text)

    speak_text(f"caption:/n{caption}/n/n sentiment is {sentiment_label}. topic is {top_topic}")
    show_bar_chart(topics)

root = tk.Tk()
root.title("img to text + uclassify analyzer")
root.geometry("500x500")

tk.Label(root, text='choose caption type', font=("Helvetica", 14)).pack(pady=10)
for i, label in enumerate(['short (5 words)', 'expanded (30 words)', 'summary (50 words)', 'exit'], start=1):
    tk.Button(root, text=label, width=30, command=lambda i=i: on_option_select(i)).pack(pady=5)

    result_label = tk.Label(root, text="", justify="left", font=("Helvetica", 12))
    result_label.pack(pady=20)

    root.mainloop()