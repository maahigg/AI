import requests

url = "https://uselessfacts.jsph.pl/random.json"

def get_random_technology_fact():
    response = requests.get(url)
    if response.status_code == 200:
        fact_data = response.json()
        print(f"did you know? {fact_data['text']}")
    else:
        print("failed to fetch fact")
    
while True:
    user_input = input("press enter to get a random technology fact or type 'q' to quit")
    if user_input.lower() == 'q':
        break

    get_random_technology_fact()