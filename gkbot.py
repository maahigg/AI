import tkinter as tk
from tkinter import messagebox, ttk, PhotoImage
import speech_recognition as sr
import pyttsx3
import random

engine = pyttsx3.init()
engine.setProperty('rate', 150)

questions = {
    "easy": [
        {"q": "What is the capital of India?", "a": "New Delhi", "options": ["Mumbai", "New Delhi", "Kolkata", "Chennai"]},
        {"q": "Which planet is known as the Red Planet?", "a": "Mars", "options": ["Earth", "Venus", "Mars", "Jupiter"]},
    ],
    "medium": [
        {"q": "What gas do plants absorb?", "a": "Carbon dioxide", "options": ["Oxygen", "Nitrogen", "Carbon dioxide", "Hydrogen"]},
        {"q": "Which vitamin is produced in sunlight?", "a": "Vitamin D", "options": ["Vitamin A", "Vitamin C", "Vitamin D", "Vitamin B12"]},
    ],
    "hard": [
        {"q": "Who discovered gravity?", "a": "Isaac Newton", "options": ["Albert Einstein", "Isaac Newton", "Galileo Galilei", "Nikola Tesla"]},
        {"q": "Which part of the cell contains DNA?", "a": "Nucleus", "options": ["Cytoplasm", "Mitochondria", "Nucleus", "Cell membrane"]},
    ]
}

score = 0
current_q = 0
selected_level = "easy"
quiz_data = []

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Please say your answer.")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        return text.strip().lower()
    except:
        speak("Sorry, I couldn't understand.")
        return ""
    
def load_question():
    global current_q
    if current_q < len(quiz_data):
        q = quiz_data[current_q]
        question_label.config(text=q["q"])

        for i, opt in enumerate(q["options"]):
            option_buttons[i].config(text=opt, state="normal")

        progress_var.set((current_q / len(quiz_data)) * 100)

        if q["img"]:
            img = PhotoImage(file=q["img"])
            image_label.config(image=img)
            image_label.image = img
        else:
            image_label.config(image="")

    else:
        messagebox.showinfo("Quiz Over", f"Your score: {score}/{len(quiz_data)}")
        speak(f"Quiz over. Your score is {score} out of {len(quiz_data)}.")
        root.quit()

def check_answer(selected):
    global score, current_q
    correct = quiz_data[current_q]['a'].lower()
    if selected.lower() == correct:
        score += 1
        speak("Correct!")
    else:
        speak(f"Wrong. The correct answer is {quiz_data[current_q]['a']}")

    current_q += 1
    load_question()

def start_quiz():
    global selected_level, quiz_data, current_q, score
    selected_level = level_var.get()
    quiz_data = random.sample(questions[selected_level], len(questions[selected_level]))
    current_q = 0
    score = 0
    load_question()

def voice_answer():
    user_voice = listen()
    for btn in option_buttons:
        if user_voice in btn.cget("text").lower():
            check_answer(btn.cget("text"))
            break

root = tk.Tk()
root.title("🧠 GK & Science Bot")
root.geometry("600x600")

tk.Label(root, text="Select Difficulty Level:").pack()
level_var = tk.StringVar(value="easy")
tk.OptionMenu(root, level_var, "easy", "medium", "hard").pack()

tk.Button(root, text="Start Quiz", command=start_quiz).pack(pady=10)

question_label = tk.Label(root, text="", font=("Helvetica", 14), wraplength=500)
question_label.pack(pady=10)

image_label = tk.Label(root)
image_label.pack()

option_buttons = []
for i in range(4):
    btn = tk.Button(root, text="", width=30, command=lambda b=i: check_answer(option_buttons[b].cget("text")))
    btn.pack(pady=5)
    option_buttons.append(btn)

tk.Button(root, text="🎤 Voice Answer", command=voice_answer).pack(pady=10)

progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100, length=400)
progress_bar.pack(pady=10)

root.mainloop()