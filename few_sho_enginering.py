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
    
def reinforcement_learning():
    print("\n=== REINFORCEMENT LEARNING ACTIVITY")
    prompt = input("enter a promp for the ai model (e.g describe the lion):")
    initial_response = generate_response(prompt)
    print(f"\ninital ai response: {initial_response}")

    rating = int(input("rate the response from 1(bad) to 5(good): "))
    feedback = input("provide feedback for improvement: ")

    improved_response = f"{initial_response} (improved with your feedback: {feedback})"
    print(f"\nimproved ai response: {improved_response}")

    print("\nreflection:")
    print("1. how did the model's response improve with feedback?\n2. how does reinforcement learning help ai to improve its performance over time?")

def role_based_prompt_activity():
    print("\n=== role based prompts activity")

    category = input("enter a category: like science, history, math, etc: ")
    item = input(f"enter a specific {category} topic: ")

    teacher_prompt = f"you are a teacher. explain {item} in simple terms."
    expert_prompt = f"you are an expert in {category}. explain {item} in a detailed, technical manner."

    teacher_response = generate_response(teacher_prompt)
    expert_response = generate_response(expert_prompt)

    print(f"\n teachers perspective: {teacher_response}")
    print(f"expert's perspective: {expert_response}")
    print("\nreflection:")
    print("1. how did the model's response differ between teacher and expert?\n2. how does reinforcement learning help ai to improve its performance over time?")

def run_activity():
    print("ai learning activity")

    activity_choice = input("which activity would u like to run?")
    if activity_choice == 1:
        reinforcement_learning()
    elif activity_choice == 2:
        role_based_prompt_activity

if __name__ == "__main__":
    run_activity()