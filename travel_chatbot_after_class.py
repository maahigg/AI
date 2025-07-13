import re, random
from colorama import Fore, init

init(autoreset=True)

destinations = {
    "beaches": ["Bali", "Maldives", "Phuket"],
    "mountains": ["Swiss Alps", "Rocky Mountains", "Himalayas"],
    "cities": ["Tokyo", "Paris", "New York"]
}

jokes = [
    "Why don't programmers like nature? Too many bugs!",
    "Why did the computer go to the doctor? Because it had a virus!",
    "Why do travelers always feel warm? Because of all their baggage!"
]

def normalize_input(text):
    return re.sub(r"\s+", " ", text.strip().lower())

def recommend():
    print(Fore.CYAN + "TravelBot: Beaches, mountains or cities?")
    preference = input(Fore.YELLOW + "You: ")
    preference = normalize_input(preference)

    if preference in destinations:
        suggestion = random.choice(destinations[preference])
        print(Fore.GREEN + f"TravelBot: How about {suggestion}?")
        print(Fore.CYAN + "TravelBot: Do you like it? (yes/no)")
        answer = input(Fore.YELLOW + "You: ").lower()

        if answer == "yes":
            print(Fore.GREEN + f"TravelBot: Awesome! Enjoy {suggestion}! ")
        elif answer == "no":
            print(Fore.RED + "TravelBot: Let's try another.")
            recommend()
    else:
        print(Fore.RED + "TravelBot: Sorry, I don't have that kind of destination")

    show_help()

def packing_tips():
    print(Fore.CYAN + "TravelBot: Where to?")
    location = normalize_input(input(Fore.YELLOW + "You: "))
    print(Fore.CYAN + "TravelBot: How many days?")
    days = input(Fore.YELLOW + "You: ")

    print(Fore.GREEN + f"TravelBot: Packing tips for {days} days in {location}:")
    print(Fore.GREEN + "- Pack versatile clothes.")
    print(Fore.GREEN + "- Bring chargers/adapters.")
    print(Fore.GREEN + "- Check the weather forecast.")

def tell_joke():
    print(Fore.YELLOW + f"TravelBot: {random.choice(jokes)}")

def weather_info():
    print(Fore.CYAN + "TravelBot: Do you want weather info for beaches, mountains, or cities?")
    place_type = input(Fore.YELLOW + "You: ").strip().lower()

    weather = {
        "beaches": "warm and sunny, you can go swimming or relax on the beach!",
        "mountains": "cool and refreshing, it can get cold.",
        "cities": "varies by location, but usually mild to moderate, remember to pack comfy shoes!"
    }

    if place_type in weather:
        print(Fore.GREEN + f"TravelBot: {weather[place_type]}")
    else:
        print(Fore.RED + "TravelBot: I don't have weather info for that category.")

def airlines():
    print(Fore.CYAN + "TravelBot: Here are some good airline options:")
    print(Fore.GREEN + "- Emirates")
    print(Fore.GREEN + "- Korean Air")
    print(Fore.GREEN + "- Singapore Airlines")
    print(Fore.GREEN + "- Turkish Airlines")
    print(Fore.GREEN + "- Lufthansa")

def hotels():
    print(Fore.CYAN + "TravelBot: Do you want hotel suggestions for beaches, mountains, or cities?")
    place_type = input(Fore.YELLOW + "You: ").strip().lower()

    hotel_recs = {
        "beaches": ["Soneva Fushi in the  Maldives", "Four Seasons in Bora Bora", "Amankila in Bali"],
        "mountains": ["Badrutts Palace in St. Moritz", "The Lodge in Verbier", "Oberoi Wildflower Hall in India"],
        "cities": ["The Ritz in Paris", "Park Hyatt in Tokyo", "The Plaza in New York"]
    }

    if place_type in hotel_recs:
        print(Fore.GREEN + "TravelBot: Here are some great hotel options:")
        for hotel in hotel_recs[place_type]:
            print(Fore.GREEN + f"- {hotel}")
    else:
        print(Fore.RED + "TravelBot: I don't have hotel suggestions for that type.")

def show_help():
    print(Fore.MAGENTA + "\nI can:")
    print(Fore.GREEN + "- Suggest travel spots (say 'recommendation')")
    print(Fore.GREEN + "- Offer packing tips (say 'packing')")
    print(Fore.GREEN + "- Tell a joke (say 'joke')")
    print(Fore.GREEN + "- Give weather info (say 'weather')")
    print(Fore.GREEN + "- Recommend airlines (say 'airlines')")
    print(Fore.GREEN + "- Suggest hotels (say 'hotels')")
    print(Fore.CYAN + "Type 'exit' or 'bye' to end.\n")

def chat():
    print(Fore.CYAN + "Hello! I'm TravelBot.")
    name = input(Fore.YELLOW + "Your name? ")
    print(Fore.GREEN + f"Nice to meet you, {name}!")

    show_help()

    while True:
        user_input = input(Fore.YELLOW + f"{name}: ")
        user_input = normalize_input(user_input)

        if "recommend" in user_input or "suggest" in user_input:
            recommend()
        elif "pack" in user_input or "packing" in user_input:
            packing_tips()
        elif "joke" in user_input or "funny" in user_input:
            tell_joke()
        elif "weather" in user_input:
            weather_info()
        elif "airline" in user_input or "flight" in user_input:
            airlines()
        elif "hotel" in user_input:
            hotels()
        elif "help" in user_input:
            show_help()
        elif "exit" in user_input or "bye" in user_input:
            print(Fore.CYAN + "TravelBot: Safe Travels! Goodbye!")
            break
        else:
            print(Fore.RED + "TravelBot: Could you rephrase?")

if __name__ == "__main__":
    chat()
