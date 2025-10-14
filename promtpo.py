import os 
import time
from google import genai
from google.generativeai import types
import config

def generate_response(prompt, temperature=0.5):
    try:
        client = genai.Client(api_key=config.GEMINI_API_KEY)
        contents = [
            types.Content(
                role="user",
                parts={
                    types.Part.from_text(prompt)
                }
            )
        ]
        generate_content_config = types.GenerateContentConfig(
            temperature=temperature,
            response_mime_type="text/plain"
        )

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=contents,
            config=generate_content_config
        )

        return response.text
    except Exception as e:
        return f"error generating response:{str(e)}"
    
def temperature_prompt_activity():
    print("=" *80)
    print("advanced prompt engineering: temperature and insturction based prompts")
    print("="*80)
    print("\nin this activity, we'll explore:")
    print("1. how temperature affects ai creativity and randomness")
    print("2. how instruction-based prompts can control ai outputs")

    print("\n" + "-" * 40)
    print("part 1: temperature exploration")
    print("\n" + "-" * 40)

    base_prompt = input("\nenter a creative prompt(eg. write a short story about a robot learning how to paint)")
    print("\nGenerating responses with different temperature settings...")
    print("\n--low temperature (0.1) more deterministic--")
    low_temp_response = generate_response(base_prompt, temperature=0.1)
    print(low_temp_response)

    time.sleep(1)

    print("--medium temperature (0.5) balanced--")
    medium_temp_response = generate_response(base_prompt, temperature=0.5)
    print(medium_temp_response)

    time.sleep(1)

    print("\n--high temperature(0.9) more random/creative--")
    high_temp_response = generate_response(base_prompt, temperature=0.9)
    print(high_temp_response)

    print("\n"+"-"*40)
    print("part 2: instruction based prompts")
    print("-"*40)

    print("\nnow, lets explore how specific instructions change the ai's output")
    topic = input("\nchoose a topic (eg. climate change, space exploration)")

    instructions = {
        f"summarize the key facts about {topic} in 3-4 sentences",
        f"explain {topic} as if im a 10 yr old",
        f"write a pro/con list about {topic}",
        f"create a fictional news headline from the year 2050 about {topic}"
        }
    
    for i, instruction in enumerate(instructions, 1):
        print(f"\n--instruction {i}: {instruction}--")
        response=generate_response(instruction, temperature=0.7)
        print(response)
        time.sleep(1)

    print("\n" + "-"*40)
    print("part 3: creating your own instruction-based prompt")
    print("-"*40)

    print("\nnow its your turn! create an instruction based prompt and test it with different temperatures.")
    
    custom_instruction = input("\nenter your instruction-based prompt")

    try:
        custom_temp = float(input("\nset a temperature(0.1 to 1.0)"))
        if custom_temp < 0.1 or custom_temp > 1.0:
            print("invalid temp, using default 0.7")
            custom_temp = 0.7
    except ValueError:
        print("invalid input, using default temp 0.7")
        custom_temp=0.7
    
    print(f"\n your custom prompt with temperaute {custom_temp}---")
    custom_response = generate_response(custom_instruction=custom_temp)
    print(custom_response)

    print("-"*40)
    print("refleciton questions")
    print("-"*40)
    print("how did changing the temperature afect the creativity and variety in the ai's response?")
    print("which instruction based prompt produced the most useful or interesting result? how might you combine specific instructions and temp settings in real life applications? what patterns did you notice in how the ai response to different types of instructions")

if __name__ == "__main__":
    temperature_prompt_activity()