import tkinter as tk
from tkinter import messagebox
import requests

API_KEY ="2SA6uoG0hDtK"

CLASSIFIERS = {
    "Gender": "uClassify/GenderAnalyzer",
    "Age": "uClassify/AgeAnalyzer"
}

def classify_text():
    user_text = entry.get()
    if not user_text.strip():
        messagebox.showwarning("Input error", "please enter some text")
        return
    
    headers = {
        'Authorization': f'Token {API_KEY}',
        'Content-Type': 'application/json'
    }

    results = ""

    for label, endpoint in CLASSIFIERS.items():
        url = f"https://api.uclassify.com/v1/{endpoint}/classify"
        data = {"texts": [user_text]}
        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            result = response.json()[0]['classification']
            results += f"\n {label} Prediction:\n"
            for item in result:
                results += f" {item['className']}: {item['p']:.2f}\n"
        except Exception as e:
            results += f"\n error with {label} classifier: {e}\n"
    
    output.config(state='normal')
    output.delete(1.0, tk.END)
    output.insert(tk.END, results)
    output.config(state='disabled')

root = tk.Tk()
root.title("text classifier: gender and age")
root.geometry("500x400")

tk.Label(root, text="enter text to classify:", font=("Arial", 12)).pack(pady=5)
entry = tk.Entry(root, width=60)
entry.pack(pady=5)

tk.Button(root, text='classify', command=classify_text).pack(pady=5)

output = tk.Text(root, height=15, width=60, state='disabled')
output.pack(pady=10)

root.mainloop()