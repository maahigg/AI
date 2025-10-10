from google import genai
import config

client = genai.Client(api_key=config.GEMINI_API_KEY)

def generate_response(prompt):
    response = client.models.generate_content(
        model="gemini-2.0-flash", 
        contents=prompt
    )
    return response.text

def silly_prompt():
    print("welcome to the ai prompt engineering tutorial")
    print("in this activity, we will learn about clarity and specificity and contextual information in crafting prompts for ai")
    print("\n lets start by creating a vague prompt, making it more specific, and then adding context")

    vague_prompt = input("\n please enter a vague prompt, eg, tell me about technology")

    print(f"\nyour vague prompt: {vague_prompt}")
    vague_response = generate_response(vague_prompt)
    print("\nAI's response to the vague prompt:")
    print(vague_response)

    specific_prompt = input("\n now make the prompt more specifc, eg, explain how ai works in self driving cars")
    print(f"\nyour specific prompt: {specific_prompt}")
    specific_response = generate_response(specific_prompt)
    print("\nai's response to the specific prompt:")
    print(specific_response)

    contextual_prompt = input("\nnow, add context to your specific prompt (eg given the advancements in autonomous vehicles, explain how ai is used in self-driving cars to make real time driving decisions)")

    print(f"\nyour contextual prompt: {contextual_prompt}")
    contextual_response = generate_response(contextual_prompt)
    print("\nai;s response to the contextual prompt: ")
    print(contextual_response)

    print("\n -- reflection --")
    print("1. how did the ai's response change when the prompt was made more specific?")
    print("2. how did the ai's response improve with the added context?")
    print("3. which prompt produced the most relevant and tailored response? why?")

silly_prompt()