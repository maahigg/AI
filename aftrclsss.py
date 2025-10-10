import speech_recognition as sr
import pyaudio
import pyttsx3
import random
import datetime

# Initialize pyttsx3 and set default voice
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Default: female
engine.setProperty('rate', 150)
user_name = ""

def speak(text):
    """Speaks the given text."""
    engine.say(text)
    engine.runAndWait()

def get_audio():
    """Listens for and converts speech to text."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print(">>> speak now...")
        audio = r.listen(source)

    try:
        command = r.recognize_google(audio)
        print(f"I got you said: {command}")
        return command.lower()
    except sr.UnknownValueError:
        print("❌ could not understand.")
        speak("Sorry, I didn't catch that.")
        return ""
    except sr.RequestError as e:
        print(f"❌ API Error: {e}")
        speak("There was a network issue.")
        return ""

def respond_to_command(command):
    """Processes the spoken command and provides a response."""
    global user_name

    # Check for "hi" or "hello"
    if "hello" in command or "hi" in command:
        if user_name:
            speak(f"Hi {user_name}, how can I help you?")
        else:
            speak("Hi there! How can I help you today?")

    # Check for "your name"
    elif "your name" in command:
        speak("I am your smart Python assistant.")

    # Check for "time"
    elif "time" in command:
        now = datetime.datetime.now()
        speak(f"the time is {now.strftime('%H:%M')}")

    # Check for "date"
    elif "date" in command:
        today = datetime.datetime.now()
        speak(f"today is {today.strftime('%B %d, %Y')}")

    # Check for "my name is" and set user_name
    elif "my name is" in command:
        user_name = command.split("my name is")[-1].strip().capitalize()
        speak(f"Nice to meet you, {user_name}!")

    # Check for "fact"
    elif "fact" in command:
        facts = [
            "Money never spoils. Archaeologists found 3000-year-old honey in Egyptian tombs!",
            "Octopuses have three hearts.",
            "Bananas are berries, but strawberries aren't.",
            "The Pacific Ocean can be a mile wide in places.",
            "Water can boil and freeze at the same time in a vacuum."
        ]
        speak(random.choice(facts))

    # Check for "use male voice"
    elif "use male voice" in command:
        engine.setProperty('voice', voices[0].id)
        speak("Switched to male voice.")

    # Check for "use female voice"
    elif "use female voice" in command:
        engine.setProperty('voice', voices[1].id)
        speak("Switched to female voice.")

    # Check for "exit" or "stop"
    elif "exit" in command or "stop" in command:
        speak("Goodbye!")
        return False

    # Default response if command is not recognized
    else:
        speak("I'm not sure how to help with that.")

    return True

def main():
    """Main loop for the assistant."""
    speak("Your voice assistant activated. Say something!")
    while True:
        command = get_audio()
        if command and not respond_to_command(command):
            break

if __name__ == "__main__":
    main()