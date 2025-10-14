import speech_recognition as sr
import pyttsx3
from googletrans import Translator

# Initialize text-to-speech engine
def speak(text, language="en"):
    # Initialise the engine
    engine = pyttsx3.init()
    # Set speed of speech
    engine.setProperty('rate', 150)
    # Get voices and set properties
    voices = engine.getProperty('voices')

    # Set voice for English or other language if supported by pyttsx3
    if language == "en":
        # Default English voice
        engine.setProperty('voice', voices[0].id)
    else:
        # Fallback to another voice if available
        engine.setProperty('voice', voices[2].id) # Fallback to another voice if available

    engine.say(text)
    engine.runAndWait()

# Speak-to-Text: Recognize spoken language
def speech_to_text():
    # Recognizer instance
    recognizer = sr.Recognizer()
    # Use microphone as source
    with sr.Microphone() as source:
        print(">>> Please speak now. <<<")
        # Listen to the source
        audio = recognizer.listen(source)

    try:
        print(">>> Recognizing speech... <<<")
        # Use Google Speech Recognition API
        text = recognizer.recognize_google(audio)
        print("✅ Said: {text}".format(text=text))
        return text
    # Handle unknown voice
    except sr.UnknownValueError:
        print("❌ Could not understand the audio.")
        return None
    # Handle API error
    except sr.RequestError as e:
        print("❌ API Error: {e}".format(e=e))
        return None

# Translate text using Google Translate API
def translate_text(text, target_language="es"):
    # Translator instance
    translator = Translator()
    # Perform translation
    translation = translator.translate(text, dest=target_language)
    # Print confirmation
    print("✅ Translated text: {translation.text}".format(translation=translation))
    return translation.text

# display language options to the user
def display_language_options():
    print("Available translation languages:")
    print("1. Hindi (hi)")
    print("2. Tamil (ta)")
    print("3. Telugu (te)")
    print("4. Spanish (es)")
    print("5. French (fr)")

    # User selects language
    language_input = input("Please select the target language number (1-5) ")
    language_dict = {
        "1": "hi",
        "2": "ta",
        "3": "te",
        "4": "es",
        "5": "fr"
    }
    # Default to Spanish if invalid input
    return language_dict.get(language_input, "es")

# Main function to combine all steps
def main():
    print("=== Real-time Speech Translation ===")

    # Step 1: Display language options and get user's choice
    target_language = display_language_options()

    # Step 2: Speech-to-Text (recognizing speech in any language)
    original_text = speech_to_text()

    if original_text:
        # Step 3: Text-to-Text (translate to selected target language)
        translated_text = translate_text(original_text, target_language=target_language)

        # Step 4: Text-to-Speech (Translate output and speak it)
        speak(translated_text, language=target_language) # Speak the translation in the target language
        print("✅ Translation spoken out!")

if __name__ == "__main__":
    main()