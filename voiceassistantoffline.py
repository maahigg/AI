import queue
import sounddevice as sd
from vosk import Model, KaldiRecognizer
import pyttsx3
import json
import datetime

model = Model("model")
recognizer = KaldiRecognizer(model, 16000)
audio_queue = queue.Queue()
tts_engine = pyttsx3.init()

def callback(indata, frames, time, status):
    if status:
        print(status)
    audio_queue.put(bytes(indata))

def speak(text):
    tts_engine.say(text)
    tts_engine.runAndWait()

with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16', 
                       channels=1, callback=callback):
    print("listening...")

    while True:
        data = audio_queue.get()
        if recognizer.AcceptWaveform(data):
            result=recognizer.Result()
            text = json.loads(result)["text"]
            print("you said:", text)

            if "time" in text:
                now = datetime.datetime.now().strftime("%H:%M")
                speak(f"the time is {now}")
            elif "date" in text:
                today=datetime.datetime.now().strftime("%A, %B, %d, %Y")
                speak(f"today is {today}")
            elif "exit" in text or "quit" or text:
                speak("goodbye!")
                break
            else:
                speak("I heard you say ", text)