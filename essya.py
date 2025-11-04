import os
from google import genai
from google.genai import types

# Initialize the Gemini API client
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

def generate_response(prompt, temperature=0.3):
    """Generate a response from Gemini API."""
    try:
        contents = [types.Content(role="user", parts=[types.Part.from_text(text=prompt)])]
        config_params = types.GenerateContentConfig(temperature=temperature)
        response = client.models.generate_content(
            model="gemini-2.5-flash", contents=contents, config=config_params
        )
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

def reinforcement_learning_activity():
    """Conducts the reinforcement learning activity."""
    print("\n--- REINFORCEMENT LEARNING ACTIVITY ---")

    # Get user input for initial response
    prompt = input("Enter a prompt for the AI model (e.g., 'Describe the lion'): ")
    initial_response = generate_response(prompt)
    print(f"\nInitial AI Response: {initial_response}")

    # Get feedback and rating
    rating = input("Rate the response from 1 (bad) to 5 (good): ")
    feedback = input("Provide feedback for improvement: ")

    # Simulate model improvement based on feedback
    improved_response = generate_response(
        f"Improved version of AI Response: {initial_response} (Improved with your feedback: {feedback})"
    )
    print(f"\nImproved AI Response: {improved_response}")

    # Reflection
    print("\n-- Reflection --")
    print("1. How did the model's response improve with feedback?")
    print("2. How does reinforcement learning help AI to improve its performance over time?")

def role_based_prompt_activity():
    """Conducts the role-based prompts activity."""
    print("\n--- ROLE-BASED PROMPTS ACTIVITY ---")

    # Get user input for roles and prompt
    category = input("Enter a category (e.g., science, history, math): ")
    item = input(f"Enter a specific (category) topic (e.g., 'photosynthesis' for science): ")

    # Generate premises for different roles
    teacher_prompt = f"Role: You are a teacher. Explain {item} in simple terms."
    expert_prompt = f"Role: You are an expert in {category}. Explain {item} in a detailed, technical manner."
    business_prompt = f"Role: You are a business leader who can explain how {item} impacts your industry."
    peer_prompt = f"Explain {item} in terms a college student would understand."

    # Get AI responses for the different roles
    teacher_response = generate_response(teacher_prompt)
    expert_response = generate_response(expert_prompt)
    business_response = generate_response(business_prompt)
    peer_response = generate_response(peer_prompt)

    print(f"\n--- Teacher's Perspective ---\n{teacher_response}")
    print(f"\n--- Expert's Perspective ---\n{expert_response}")
    print(f"\n--- Business Leader's Perspective ---\n{business_response}")
    print(f"\n--- Peer Student's Perspective ---\n{peer_response}")

    # Reflection
    print("\n-- Reflection --")
    print("1. How did the AI's response differ between the teacher's and expert's perspectives?")
    print("2. How can role-based prompts help tailor AI responses for different contexts?")

def run_activity():
    """Runs the entire activity for the user."""
    print("\n=== AI Learning Activity ===")

    # Choose activity
    activity_choice = input("Which activity would you like to run? (1: Reinforcement Learning, 2: Role-Based Prompts): ")

    if activity_choice == "1":
        reinforcement_learning_activity()
    elif activity_choice == "2":
        role_based_prompt_activity()
    else:
        print("Invalid choice. Please choose either 1 or 2.")

if __name__ == "__main__":
    run_activity()