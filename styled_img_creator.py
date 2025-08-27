# styled_image_creator.py

import requests
from PIL import Image, ImageEnhance, ImageFilter
from io import BytesIO
from config import HF_API_KEY


def generate_image_from_text(prompt: str) -> Image.Image:
    """
    Sends a text prompt to the Stable Diffusion API
    and returns the generated image as a Pillow Image.
    """
    API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-3-medium-diffusers"
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    payload = {"inputs": prompt}

    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        return Image.open(BytesIO(response.content))
    else:
        raise Exception(
            f"Request failed with status code {response.status_code}: {response.text}"
        )


def daylight_effect(image: Image.Image) -> Image.Image:
    """
    Brightens, slightly enhances contrast, and applies a soft blur
    to create a 'daylight edition' effect.
    """
    image = ImageEnhance.Brightness(image).enhance(1.3)   # +30% brightness
    image = ImageEnhance.Contrast(image).enhance(1.1)     # +10% contrast
    image = image.filter(ImageFilter.GaussianBlur(radius=1))  # Soft blur
    return image


def night_mood_effect(image: Image.Image) -> Image.Image:
    """
    Darkens brightness slightly, increases contrast, and applies
    a very subtle blur to create a 'night mood' effect.
    """
    image = ImageEnhance.Brightness(image).enhance(0.9)   # 10% darker
    image = ImageEnhance.Contrast(image).enhance(1.4)     # +40% contrast
    image = image.filter(ImageFilter.GaussianBlur(radius=0.5))  # Subtle blur
    return image


def main():
    print("=== Welcome to the AI Image Stylist Project! ===")
    prompt = input("Enter your image description:\n> ").strip()

    try:
        print("\nGenerating your base image...")
        image = generate_image_from_text(prompt)

        # Apply Daylight Edition style
        print("Applying Daylight Edition style...")
        daylight_img = daylight_effect(image)
        daylight_img.show()
        daylight_img.save(f"{prompt.replace(' ', '_')}_daylight.png")
        print("Daylight Edition saved.\n")

        # Apply Night Mood style
        print("Applying Night Mood style...")
        night_img = night_mood_effect(image)
        night_img.show()
        night_img.save(f"{prompt.replace(' ', '_')}_night.png")
        print("Night Mood saved.\n")

    except Exception as e:
        print(f"⚠️ Something went wrong: {e}")


if __name__ == "__main__":
    main()
