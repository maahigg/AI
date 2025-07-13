import colorama
from colorama import Fore, Style
import textblob
from textblob import TextBlob

colorama.init(autoreset=True)

print(f"{Fore.CYAN}Welcome to Sentiment Spy!")

user_name = input(f"{Fore.MAGENTA}Please enter your name: ").strip()
if not user_name:
    user_name = "Mystery Agent"

conversation_history = []   

print(f"\n{Fore.CYAN}Hello, Agent {user_name}!")
print(f"Type a sentence and I will analyze your sentiment using TextBlob.")
print(f"Type {Fore.YELLOW}'reset'{Fore.CYAN}, {Fore.YELLOW}'history'{Fore.CYAN}, or {Fore.YELLOW}'exit'{Fore.CYAN} to use commands.\n")

while True:
    user_input = input(f"{Fore.GREEN}>> ").strip()

    if not user_input:
        print(f"{Fore.RED}Please enter some text or a valid command.")
        continue

    if user_input.lower() == "exit":
        print(f"\n{Fore.BLUE}Exiting Sentiment Spy. Farewell, Agent {user_name}!")
        break

    elif user_input.lower() == "reset":
        conversation_history.clear()
        print(f"{Fore.CYAN}All conversation history cleared!")
        continue

    elif user_input.lower() == "history":
        if not conversation_history:
            print(f"{Fore.YELLOW}No conversation history yet.")
        else:
            print(f"{Fore.CYAN}Conversation History:")
            for idx, (text, polarity, sentiment_type) in enumerate(conversation_history, start=1):
                if sentiment_type == "Positive":
                    color = Fore.GREEN
                    emoji = "😀"
                elif sentiment_type == "Negative":
                    color = Fore.RED
                    emoji = "😠"
                else:
                    color = Fore.YELLOW
                    emoji = "😐"    

                print(f"{idx}. {color}{emoji} {text} (Polarity: {polarity:.2f}, {sentiment_type})")
        continue

    polarity = TextBlob(user_input).sentiment.polarity

    if polarity > 0.25:
        sentiment_type = "Positive"
        color = Fore.GREEN
        emoji = "😀"
    elif polarity < -0.25:
        sentiment_type = "Negative"
        color = Fore.RED
        emoji = "😠"
    else:
        sentiment_type = "Neutral"
        color = Fore.YELLOW
        emoji = "😐"       
    
    conversation_history.append((user_input, polarity, sentiment_type))

    print(f"{color}{emoji} {sentiment_type} sentiment detected! (Polarity: {polarity:.2f})")


