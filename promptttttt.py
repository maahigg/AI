from google import genai  # Use this for Google Gemini API
import config  # Contains your API Key

# Initialize client
client = genai.Client(api_key=config.GEMINI_API_KEY)

# Function to get response
def generate_response(prompt):
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )
    return response.text

# Tutorial Activity
def prompt_engineering_activity():
    print("Welcome to the AI Prompt Engineering Tutorial")

    vague_prompt = input("Enter a vague prompt: ")
    print("\nAI's response to vague prompt:")
    print(generate_response(vague_prompt))

    specific_prompt = input("\nNow, make it more specific: ")
    print("\nAI's response to specific prompt:")
    print(generate_response(specific_prompt))

    contextual_prompt = input("\nNow, add context to your specific prompt: ")
    print("\nAI's response to contextual prompt:")
    print(generate_response(contextual_prompt))

    print("\n--- Reflection ---")
    print("1. How did the AI's response change when the prompt was made more specific?")
    print("2. How did the AI's response improve with the added context?")
    print("3. Which prompt produced the most relevant and tailored response? why?")