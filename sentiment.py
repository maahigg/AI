import colorama
from colorama import Fore, Style
import textblob
from textblob import TextBlob

colorama.init()

def welcome():
    print(Fore.CYAN + f"Welcome to Sentiment Spy!")

username = input(Fore.MAGENTA + f"What is your name?").strip()

if not username:
    username = "Mystery Agent"

conversation_history = []

print(Fore.LIGHTGREEN_EX + f"The available commands are:")
print(Fore.LIGHTCYAN_EX + f"type 'reset to reset conversation history.")
print(Fore.LIGHTCYAN_EX + f"type 'history' to see the conversation history.")
print (Fore.LIGHTCYAN_EX + f"type 'exit' to exit")

while True:
    user_input = input(f"")


