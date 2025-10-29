import os
from google import generativeai
from google.generativeai import types
import config

client = generativeai.Client(api_key = config.GEMINI_API_KEY)

def generate_response(prompt, temperature = 0.3):
    try:
        contents = [types.Content(role="user", parts=[types.Part.from_text(text=prompt)])]
        config_params = types.GenerateContentConfig(temperature=temperature)
        response = client.models.generate_content(
            model="gemini-2.0-flash", contents=contents, config = config_params)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"
    
def bias_mitigation_activity():
    print("\n===bias mitigation activity===\n")
    prompt = input("enter a prompt to explore bias, eg. describe the ideal doctor")
    initial_response = generate_response(prompt)
    print(f"\ninitial ai response: {initial_response}")

    modified_prompt = input("modify the prompt to make it more neutral, eg. describe the qualities of a doctor")
    modified_response = generate_response(modified_prompt)
    print(f"\nmodified ai response: {modified_response}")

def token_limit_activity():
    print("\n=== token limit activity ===")
    long_prompt = input("enter a long prompt (more than 300 words, eg. a detailed story or description)")
    long_response = generate_response(long_prompt)
    print(f"\nresponse to long prompt: {long_response[:500]}")

    short_prompt = input("now, condence the prompt to be more concise: ")
    short_response = generate_response(short_prompt)
    print(f"\nresponse to condensed prompt: {short_response}")

def run_activity():
    print("\n=== ai learning activity ===")

    activity_choice = input("which activity would you like to run? 1: bias mitigation and 2: token limit activity")

    if activity_choice == 1:
        bias_mitigation_activity()
    elif activity_choice == 2:
        token_limit_activity
    else:
        print("invalid choice. please choose either 1 or 2")
        activity_choice=input("try again.")

if __name__ == "__main__":
    run_activity()