import random
from colorama import init, Fore, Style

init(autoreset=True)

def get_player_choice():
    choice = ""
    while choice not in ['rock', 'paper', 'scissors']:
        choice = input(Fore.GREEN + "Choose Rock, Paper, or Scissors: " + Style.RESET_ALL).lower()
    return choice

def get_ai_choice():
    return random.choice(['rock', 'paper', 'scissors'])

def display_choices(player, ai):
    print(Fore.CYAN + f"\nYou chose: {Fore.YELLOW}{player}")
    print(Fore.CYAN + f"AI chose: {Fore.MAGENTA}{ai}")

def determine_winner(player, ai):
    if player == ai:
        return "tie"
    elif (player == "rock" and ai == "scissors") or \
         (player == "scissors" and ai == "paper") or \
         (player == "paper" and ai == "rock"):
        return "player"
    else:
        return "ai"

def display_result(result, player_name):
    if result == "tie":
        print(Fore.YELLOW + "It's a tie!")
    elif result == "player":
        print(Fore.GREEN + f"{player_name}, you win! 🎉")
    else:
        print(Fore.RED + "AI wins! Better luck next time!")

def rock_paper_scissors():
    print(Fore.CYAN + "Welcome to Rock, Paper, Scissors!")
    player_name = input(Fore.LIGHTGREEN_EX + "Enter your name: ").strip()
    if not player_name:
        player_name = "Player"

    while True:
        player_choice = get_player_choice()
        ai_choice = get_ai_choice()

        display_choices(player_choice, ai_choice)
        result = determine_winner(player_choice, ai_choice)
        display_result(result, player_name)

        again = input(Fore.LIGHTCYAN_EX + "\nDo you want to play again? (yes/no): ").lower()
        if again != "yes":
            print(Fore.CYAN + "\nThanks for playing! Goodbye!")
            break

if __name__ == "__main__":
    rock_paper_scissors()
