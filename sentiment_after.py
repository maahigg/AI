import colorama
from colorama import Fore, Style
from textblob import TextBlob

colorama.init(autoreset=True)

def welcome():
    print(Fore.CYAN + "Welcome to Sentiment Spy!")

welcome()

username = input(Fore.MAGENTA + "What is your name? ").strip()

if not username:
    username = "Mystery Agent"

conversation_history = []

print(Fore.LIGHTGREEN_EX + "The available commands are:")
print(Fore.LIGHTCYAN_EX + "Type 'reset' to reset conversation history.")
print(Fore.LIGHTCYAN_EX + "Type 'history' to see the conversation history.")
print(Fore.LIGHTCYAN_EX + "Type 'exit' to exit.")

while True:
    user_input = input(Fore.WHITE + "").strip()

    if user_input.lower() == "exit":
        print(Fore.LIGHTMAGENTA_EX + "Goodbye, Agent.")
        break

    elif user_input.lower() == "reset":
        conversation_history.clear()
        print(Fore.YELLOW + "Conversation history cleared.")

    elif user_input.lower() == "history":
        if not conversation_history:
            print(Fore.LIGHTBLACK_EX + "No messages yet.")
        else:
            print(Fore.LIGHTWHITE_EX + "\nConversation History:")
            for i, msg in enumerate(conversation_history, 1):
                print(f"{i}. {msg}")

    elif user_input == "":
        continue

    else:
        blob = TextBlob(user_input)
        polarity = blob.sentiment.polarity
        if polarity > 0.1:
            sentiment = "Positive"
            color = Fore.GREEN
        elif polarity < -0.1:
            sentiment = "Negative"
            color = Fore.RED
        else:
            sentiment = "Neutral"
            color = Fore.YELLOW

        response = f"Sentiment: {sentiment}"
        conversation_history.append(f"{username}: {user_input} | {response}")
        print(color + response)
