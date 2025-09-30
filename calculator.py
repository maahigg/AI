import tkinter as tk
from tkinter import messagebox, scrolledtext
import pyttsx3
import math
import re

engine = pyttsx3.init()
engine.setProperty('rate', 150)

history = []

def speak(text):
    engine.say(text)
    engine.runAndWait()

def add():
    try:
        a = float(entry1.get())
        b = float(entry2.get())
        result = a + b
        show_result(f"{a} + {b} = {result}")
    except:
        show_result("invalid input")

def multiply():
    try:
        a = float(entry1.get())
        b = float(entry2.get())
        result = a * b
        show_result(f"{a} x {b} = {result}")
    except:
        show_result("invalid input")

def subtract():
    try:
        a = float(entry1.get())
        b = float(entry2.get())
        result = a - b
        show_result(f"{a} - {b} = {result}")
    except:
        show_result("invalid input")

def divide():
    try:
        a = float(entry1.get())
        b = float(entry2.get())
        if b == 0:
            show_result("error: division by 0 not possible")
        else:
            result = a / b
            show_result(f"{a} / {b} = {result}")
    except:
        show_result("invalid input")

def square_root():
    try:
        a = float(entry1.get())
        if a < 0:
            show_result("error: negative number")
        else:
            result = math.sqrt(a)
            show_result(f"sqrt({a}) = {result}")
    except:
        show_result("invalid input")

def solve_equation():
    eq = entry_eq.get()
    try:
        match = re.match(r"(\d*)x([+-]\d+)?=(\d+)", eq.replace(" ", ""))
        if match:
            a = int(match.group(1)) if match.group(1) else 1
            b = int(match.group(2)) if match.group(2) else 0
            c = int(match.group(3))
            x = (c - b) / a
            show_result(f"solution: x = {x}")
        else:
            show_result("invalid format, use ax + b = c")
    except:
        show_result("error solving equation")

def show_result(text):
    result_label.config(text=text)
    history.append(text)
    history_box.insert(tk.END, text + "\n")
    speak(text)

def clear_history():
    history.clear()
    history_box.delete("1.0", tk.END)
    result_label.config(text="history cleared")
    speak("history cleared")

root = tk.Tk()
root.title("mathbot")
root.geometry("600x600")

tk.Label(root, text="enter number 1: ").pack()
entry1 = tk.Entry(root)
entry1.pack()

tk.Label(root, text="enter number 2: ").pack()
entry2 = tk.Entry(root)
entry2.pack()

tk.Label(root, text="choose operation").pack(pady=5)
tk.Button(root, text="add", command=add).pack()
tk.Button(root, text="subtract", command=subtract).pack()
tk.Button(root, text="multiply", command=multiply).pack()
tk.Button(root, text="divide", command=divide).pack()
tk.Button(root, text="square root (of number 1)", command=square_root).pack()

tk.Label(root, text="solve equation").pack(pady=10)
entry_eq = tk.Entry(root, width=30)
entry_eq.pack()
tk.Button(root, text="solve", command=solve_equation).pack()

result_label = tk.Label(root, text="", font=("Helvetica", 12), fg="blue")
result_label.pack(pady=10)

tk.Label(root, text="history of calculations").pack()
history_box = scrolledtext.ScrolledText(root, width=60, height=10)
history_box.pack()
tk.Button(root, text="clear history", command=clear_history).pack(pady=5)

root.mainloop()