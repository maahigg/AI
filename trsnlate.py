import speech_recognition as sr
import pyttsx3
from googletrans import Translator

def speak(text, language="en"):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    voices = engine.getProperty(voices)

    if language == "en":
        engine.setProperty('voice', voices[0].id)
    else:
        engine.setProperty('voice', voices[1].id)
        
    engine.say(text)
    engine.runAndWait()

def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("? please speak now in english..")
        audio = recognizer.listen(source)

    try:
        print("? recognizing speech..")
        text=recognizer.recognize_google(audio, language="en-US")
        print(f"you said {text}")
        return text
    except sr.UnknownValueError:
        print("could not understand the audio")
    except sr.RequestError as e:
        print("api error: {e}")
    return ""

def translate_text(text, target_language="es"):
    translator = Translator()
    translation = translator.translate(text, dest=target_language)
    print(f"translated text: {translation}")
    return translation

def display_language_options():
    print(" available translation languages: \n1. Hindi (hi)\n2. Tamil (ta)\n3. Telugu (te)\n4. Bengali (bn)\n 5. Marathi (mr)\n6. Gujurati (gu)\n7. Malayalam (ml)\n8. Punjabi (pa)\n")

    choice=input("please select the target translate number (1-8)")
    language_dict = {
        "1": "hi",
        "2": "ta",
        "3": "te",
        "4": "bn", 
        "5": "mr",
        "6": "gu",
        "7": "ml",
        "8": "pa"
    }

    return language_dict.get(choice, "es")

def main():
    target_language = display_language_options()
    original_text = speech_to_text()

    if original_text:
        translated_text = translate_text(original_text, target_language=target_language)

        speak(translated_text, language="en")
        print("translation spoken out")
    
if __name__ == "__main__":
    main()