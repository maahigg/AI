import requests
from PIL import Image
from io import BytesIO
from config import HF_API_KEY, TEXT_GEN_MODEL_ID, TEXT_TO_IMAGE_MODEL_ID, CAPTION_MODEL_ID

# Generate Text Function
def generate_text(prompt: str) -> str:
    url = f"https://api-inference.huggingface.co/models/{TEXT_GEN_MODEL_ID}"
    headers = {"Authorization": f"Bearer {HF_API_KEY}", "Accept": "application/json"}
    payload = {"inputs": prompt, "parameters": {"max_new_tokens": 50, "temperature": 0.7, "do_sample": True}}

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    result = response.json()
    return result[0].get("generated_text", "").strip()

# Generate Image Function
def generate_image(prompt: str) -> bytes:
    url = f"https://api-inference.huggingface.co/models/{TEXT_TO_IMAGE_MODEL_ID}"
    headers = {"Authorization": f"Bearer {HF_API_KEY}", "Accept": "image/png"}
    payload = {"inputs": prompt}

    response = requests.post(url, headers=headers, json=payload, stream=True)
    response.raise_for_status()
    return response.content

# Caption Image Function
def caption_image(image_bytes: bytes) -> str:
    url = f"https://api-inference.huggingface.co/models/{CAPTION_MODEL_ID}"
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}

    response = requests.post(url, headers=headers, data=image_bytes)
    response.raise_for_status()
    result = response.json()
    return result[0].get("generated_text", "").strip()

def main():
    # Collect user input for prompt
    user_prompt = input("Enter a short prompt or story idea: ")
    if not user_prompt.strip():
        print("No prompt entered. Exiting.")
        return

    print("\n=== Generating Text ===")
    text_prompt = generate_text(user_prompt)
    print("Generated Text Prompt:\n", text_prompt)

    print("\n=== Generating Image ===")
    image_data = generate_image(text_prompt)
    with open("generated_image.png", "wb") as f:
        f.write(image_data)
    img = Image.open(BytesIO(image_data))
    img.show()

    print("\n=== Captioning the Generated Image ===")
    final_caption = caption_image(image_data)
    print("Final AI-Generated Caption:\n", final_caption)

if __name__ == "__main__":
    main()
