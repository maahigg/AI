import tkinter as tk
import requests
import pyttsx3

def fetch_fact():
    url = "https://uselessfacts.jsph.pl/random.json?language=en"
    try:
        response = requests.get(url)
        data = response.json()
        fact = data['text']
        fact_label.config(text=fact)
    except Exception as e:
        fact_label.config(text="failed to fetch fact")

def speak_fact():
    engine = pyttsx3.init()
    engine.say(fact_label.cget("text"))
    engine.runAndWait()

def copy_to_clipboard():
    root.clipboard_clear()
    root.clipboard_append(fact_label.cget("text"))
    root.update()

root = tk.Tk()
root.title("fact frenzy")
root.geometry("500x300")
#root.configure(bg = "f0f0f0")

title = tk.Label(root, text = "useless fact generator", font = ("Helvetica", 16, "bold"))
title.pack(pady = 10)

fact_label = tk.Label(root, text="click below to get a fact!", wraplength=450, justify="center")
fact_label.pack(pady = 20)

btn_frame = tk.Frame(root)
btn_frame.pack()

fetch_btn = tk.Button(btn_frame, text = "new fact", command= fetch_fact)
fetch_btn.grid(row = 0, column = 0, padx = 10)

copy_btn = tk.Button(btn_frame, text = "copy", command = copy_to_clipboard)
copy_btn.grid(row = 0, column = 0, padx = 10)

speak_btn = tk.Button(btn_frame, text = "speak", command = speak_fact)
speak_btn.grid(row = 0, column = 2, padx = 10)

root.mainloop()