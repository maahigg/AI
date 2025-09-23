from config import HF_API_KEY
import requests, io, json
from PIL import Image
from colorama import Fore, Style, init
init(autoreset=True)

def get_caption(image):
    url = "https://api-inference.huggingface.co/models/nlpconnect/vit-gpt2-image-captioning"
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    buf = io.BytesIO()
    image.save(buf, format="JPEG")
    res = requests.post(url, headers=headers, data=buf.getvalue())
    return res.json()[0]["generated_text"]

def expand_caption(caption):
    url = "https://api-inference.huggingface.co/models/gpt2"
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    payload = {
        "inputs": f"Expand this caption into 30 words: {caption}",
        "parameters": {"max_new_tokens": 50}
    }
    res = requests.post(url, headers=headers, json=payload)
    text = json.loads(res.content)[0]["generated_text"]
    return " ".join(text.split()[:30])

def main():
    path = input("Enter image path: ").strip()
    try:
        image = Image.open(path)
        print(Fore.YELLOW + "Generating caption...")
        caption = get_caption(image)
        print(Fore.GREEN + "Caption: " + Style.BRIGHT + caption)

        more = input("Expand to 30 words? (y/n): ").strip().lower()
        if more == "y":
            print(Fore.YELLOW + "Expanding...")
            description = expand_caption(caption)
            print(Fore.GREEN + "Expanded: " + Style.BRIGHT + description)
    except Exception as e:
        print(Fore.RED + f"Error: {e}")

if __name__ == "__main__":
    main()
