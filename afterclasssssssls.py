import os
from google import genai
from google.genai import types
import config
from colorama import init, Fore, Style

init(autoreset=True)

client = genai.Client(api_key=config.GEMINI_API_KEY)

def generate_response(prompt, temperature=0.5):
    try:
        contents = [types.Content(role="user", parts=[types.Part.from_text(text=prompt)])]
        config_params = types.GenerateContentConfig(
            temperature=temperature,
            response_mime_type="text/plain"
        )
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=contents,
            config=config_params,
        )
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

def get_essay_details():
    print(Fore.CYAN + "\n=== AI Writing Assistant ===\n")

    topic = input(Fore.YELLOW + "What is the topic of your essay? ")
    essay_type = input(Fore.YELLOW + "What type of essay are you writing? (e.g., Argumentative, Expository, Descriptive, Persuasive, Analytical) ")

    print(Fore.YELLOW + "\nSelect desired essay word count:")
    print("1. Short (≈300 words)")
    print("2. Medium (≈600 words)")
    print("3. Long (≈1000+ words)")
    word_count_choice = input(Fore.YELLOW + "Enter the number corresponding to your choice: ")
    word_length_map = {"1": 300, "2": 600, "3": 1000}
    target_word_count = word_length_map.get(word_count_choice, 300)

    target_audience = input(Fore.YELLOW + "Who is the target audience for your essay? (e.g., High school students, College professors) ")
    specific_points = input(Fore.YELLOW + "Do you have any specific points that must be included in the essay? ")

    stance = input(Fore.YELLOW + "What is your stance on the topic? (e.g., For, Against, Neutral) ")
    references = input(Fore.YELLOW + "Are there any sources, quotes, or references you'd like to include? ")
    writing_style = input(Fore.YELLOW + "Do you have any preferences for writing style? (e.g., Formal, Conversational, Academic, Creative) ")

    outline_needed = input(Fore.YELLOW + "Would you like the AI to suggest an outline first? (yes/no) ").lower()

    return {
        "topic": topic,
        "essay_type": essay_type,
        "target_word_count": target_word_count,
        "target_audience": target_audience,
        "specific_points": specific_points,
        "stance": stance,
        "references": references,
        "writing_style": writing_style,
        "outline_needed": outline_needed
    }

def generate_essay_content(details):
    temperature = float(input(Fore.YELLOW + "Enter temperature (0.1–1.0): "))

    if details["outline_needed"] == "yes":
        outline_prompt = f"Create a detailed outline for a {details['essay_type']} essay about '{details['topic']}' with a stance of '{details['stance']}'."
        outline = generate_response(outline_prompt, temperature)
        print(Fore.CYAN + "\n=== Generated Outline ===")
        print(Fore.GREEN + outline)
        input(Fore.YELLOW + "\nPress Enter to continue with essay generation...")

    intro_prompt = f"Write an engaging introduction for a {details['essay_type']} essay about '{details['topic']}' on the topic of '{details['stance']}'."
    introduction = generate_response(intro_prompt, temperature)
    print(Fore.CYAN + "\n=== Generated Introduction ===")
    print(Fore.GREEN + introduction)

    body_choice = input(Fore.YELLOW + "Would you like a step-by-step or full draft body? (step/full): ").lower()
    if body_choice == "full":
        body_prompt = f"Write the full body section for a {details['essay_type']} essay about '{details['topic']}' with the stance '{details['stance']}'."
        body = generate_response(body_prompt, temperature)
        print(Fore.CYAN + "\n=== Generated Body ===")
        print(Fore.GREEN + body)
    else:
        body_prompt = f"Step-by-step: Write body arguments for '{details['topic']}' ({details['stance']}). Explain reasoning in each step."
        body = generate_response(body_prompt, temperature)
        print(Fore.CYAN + "\n=== Step-by-Step Body ===")
        print(Fore.GREEN + body)

    conclusion_prompt = f"Write a conclusion for a {details['essay_type']} essay about '{details['topic']}' with the stance '{details['stance']}'."
    conclusion = generate_response(conclusion_prompt, temperature)
    print(Fore.CYAN + "\n=== Generated Conclusion ===")
    print(Fore.GREEN + conclusion)

def feedback_and_refinement():
    satisfaction = input(Fore.YELLOW + "How satisfied are you with the generated content? (Rate 1–5): ")
    if satisfaction != "5":
        feedback = input(Fore.YELLOW + "Please provide feedback for improvement (tone, structure, etc.): ")
        print(Fore.CYAN + f"\nThank you! We’ll refine the essay based on: {feedback}")
    else:
        print(Fore.CYAN + "\nThank you! The essay looks good.")

def run_activity():
    print(Fore.CYAN + "\nWelcome to the AI Writing Assistant!")
    details = get_essay_details()
    generate_essay_content(details)
    feedback_and_refinement()

if __name__ == "__main__":
    run_activity()
