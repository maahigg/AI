import time
from google import genai
from google.genai import types
import config

def generate_response(prompt, temperature=0.5):
    try:
        client = genai.Client(api_key=config.GEMINI_API_KEY)

        contents = [
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=prompt)],
            ),
        ]

        generate_content_config = types.GenerateContentConfig(
            temperature=temperature,
            response_mime_type="text/plain",
        )

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=contents,
            config=generate_content_config,
        )

        return response.text
    except Exception as e:
        return f"Error generating response: {str(e)}"

def temperature_prompt_activity():
    print("=" * 80)
    print("ADVANCED PROMPT ENGINEERING: TEMPERATURE & INSTRUCTION-BASED PROMPTS")
    print("=" * 80)

    print("\n" + "-" * 40)
    print("PART I: TEMPERATURE EXPLORATION")
    print("-" * 40)
    base_prompt = input("\nEnter a creative prompt (e.g., 'write a short story about a robot learning to paint'): ")

    print("\nGenerating responses with different temperature settings...")

    print("\n-- LOW TEMPERATURE (0.1) --")
    print(generate_response(base_prompt, temperature=0.1))
    time.sleep(1)

    print("\n-- MEDIUM TEMPERATURE (0.5) --")
    print(generate_response(base_prompt, temperature=0.5))
    time.sleep(1)

    print("\n-- HIGH TEMPERATURE (0.9) --")
    print(generate_response(base_prompt, temperature=0.9))
    time.sleep(1)

    print("\n" + "-" * 40)
    print("PART II: INSTRUCTION-BASED PROMPTS")
    print("-" * 40)
    topic = input("\nChoose a topic (e.g., 'climate change', 'space exploration'): ")

    instructions = [
        f"Summarize the key facts about {topic} in 3-4 sentences.",
        f"Explain {topic} as if I’m a 10-year-old child.",
        f"Write a pro/con list about {topic}.",
        f"Create a fictional news headline from the year 2050 about {topic}.",
    ]

    for i, instruction in enumerate(instructions, 1):
        print(f"\n-- INSTRUCTION {i}: {instruction} --")
        print(generate_response(instruction, temperature=0.7))
        time.sleep(1)

    print("\n" + "-" * 40)
    print("PART III: CREATE YOUR OWN PROMPT")
    print("-" * 40)

    custom_instruction = input("\nEnter your instruction-based prompt: ")
    try:
        custom_temp = float(input("Set a temperature (0.1 to 1.0): "))
        if custom_temp < 0.1 or custom_temp > 1.0:
            print("Invalid temperature. Using default 0.7.")
            custom_temp = 0.7
    except ValueError:
        print("Invalid input. Using default temperature 0.7.")
        custom_temp = 0.7

    print(f"\n-- YOUR CUSTOM PROMPT WITH TEMPERATURE {custom_temp} --")
    print(generate_response(custom_instruction, temperature=custom_temp))

    print("\n" + "-" * 40)
    print("REFLECTION QUESTIONS")
    print("-" * 40)
    print("1. How did changing the temperature affect the creativity and variety?")
    print("2. Which instruction-based prompt produced the most useful or creative result?")
    print("3. How would you use temperature and instructions for a real-world task?")
    print("4. What surprised you about the AI’s behavior with these changes?")

if __name__ == "__main__":
    temperature_prompt_activity()
