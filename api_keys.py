import tkinter as tk
import requests

API_KEY = '2SA6uoG0hDtK'

HEADERS = {
    "Authorization": f"Token {API_KEY}",
    "Content-Type": "application/json"
}

def classify_uclassify(text, classifier):
    url = f"https://api.uclassify.com/v1/uClassify/{classifier}/classify"
    response = requests.post(url, headers=HEADERS, json = {"texts": [text]})
    if response.status_code == 200:
        return {label['className']: label['p'] for label in response.json()[0]['classification']}
    else:
        return {"error": response.text}

def classify_text():
    text = input_box.get("1.0", tk.END).strip()
    if not text:
        return
    
    sentiment_result = classify_uclassify(text, "Sentiment")
    topic_result = classify_uclassify(text, "Topics")

    sentiment_output.delete("1.0", tk.END)
    sentiment_output.insert(tk.END, "sentiment analysis\n")
    for label, score in sentiment_result.items():
        sentiment_output.insert(tk.END, f"{label}: {score:.2f}\n")
    
    topic_output.delete("1.0", tk.END)
    topic_output.insert(tk.END, "topic classification\n")
    for label, score in topic_result.items():
        topic_output.insert(tk.END, f"{label}: {score:.2f}\n")

root = tk.Tk()
root.title("text classifier (sentiment and topic)")
root.geometry("600x600")

tk.Label(root, text="enter your text below:", font=("Arial", 12)).pack(pady=5)
input_box = tk.Text(root, height=5, width = 70, font=("Arial", 11))
input_box.pack(pady=5)

tk.Button(root, text = "Classify", command=classify_text, font=("Arial", 12)).pack(pady=10)
sentiment_output = tk.Text(root, height = 10, width= 70, font = ("Courier", 10))
sentiment_output.pack(pady=5)

topic_output = tk.Text(root, height = 10, width = 70, font = ("Courier", 10))
topic_output.pack(pady=5)

root.mainloop()