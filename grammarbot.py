import tkinter as tk
from tkinter import filedialog, scrolledtext
import pyttsx3
import language_tool_python
 
engine = pyttsx3.init()
engine.setProperty('rate, 150')

language_map = {
    "English": "en-US",
    "Hindi": "hi-IN",
    "French": "fr"
}
tool = language_tool_python.LanguageTool('en-US')

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak("please speak your sentence")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            input_entry.delete(0, tk.END)
            input_entry.insert(0, text)
        except sr.UnknownValueError:
            speak("sorry, i couldn't understand")
        except sr.RequestError:
            speak("speech service error")

def check_grammar():
    text = input_entry.get()
    selected_lang = lang_var.get()
    tool = language_tool_python.LanguageTool(language_map[selected_lang])
    matches = tool.check(text)
    corrected = language_tool_python.utils.correct(text, matches)

    suggestion_box.delete(1.0, tk.END)
    for match in matches:
        suggestion_box.insert(tk.END, f"- {match.message}\n")
    
    result_label_config(text=f"corrected:\n{corrected}")
    speak(f"the corrected sentence is {corrected}")

def save_to_file():
    corrected_text = result_label.cget("text").replace("corrected: \n", " ")
    if corrected_text.strip():
        file_path = filedialog.asksaveasfilename(defaultextension=".txt")
        if file_path:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(corrected_text)
            speak("corrected sentence saved successfully")
    else:
        speak("no corrected sentence to save")

root = tk.Tk()
root.title("grammar bot")
root.geometry("600x600")

tk.Label(root, text="enter a sentence").pack(pady=5)
input_entry = tk.Entry(root, width=60)
input_entry.pack(pady=5)

tk.Button(root, text="voice input", command=listen).pack(pady=5)

tk.Label(root, text="select language").pack()
lang_var = tk.StringVar(value="English")
tk.OptionMenu(root, lang_var, *language_map.keys()).pack()

tk.Button(root, text="check grammar", command=check_grammar).pack(pady=10)
result_label = tk.Label(root, text="", wraplength=500, justify="left")
result_label.pack(pady=10)

tk.Label(root, text="suggestions").pack()
suggestion_box = scrolledtext.ScrolledText(root, width=70, height=10)
suggestion_box.pack()

tk.Button(root, text="save corrected sentence", command=save_to_file).pack(pady=10)

root.mainloop()