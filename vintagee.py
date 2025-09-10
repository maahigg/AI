import requests
from PIL import Image
from io import BytesIO
from config import HF_API_KEY

API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-inpainting"
HEADERS = {"Authorization": f"Bearer {HF_API_KEY}"}

def generate_inpainting_image(prompt, image_path, mask_path):
    with open(image_path, "rb") as img_f:
        image_data = img_f.read()
    with open(mask_path, "rb") as mask_f:
        mask_data = mask_f.read()

    payload = {"inputs": prompt}
    files = {
        "image": ("image.png", image_data, "image/png"),
        "mask": ("mask.png", mask_data, "image/png")
    }

    r = requests.post(API_URL, headers=HEADERS, data=payload, files=files)
    if r.status_code == 200:
        return Image.open(BytesIO(r.content))
    raise Exception(f"{r.status_code}: {r.text}")

def main():
    print("=== Vintage Photo Healer ===")
    prompt = input("Describe the restoration (or type 'exit'): ").strip()
    if prompt.lower() == "exit":
        return

    try:
        fixed = generate_inpainting_image(prompt, "old_photo.png", "old_photo_mask.png")
        fixed.show()
        if input("Save restored image? (yes/no): ").strip().lower() == "yes":
            fixed.save("old_photo_restored.png")
            print("Saved as old_photo_restored.png")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
