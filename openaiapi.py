#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

import requests
import openai
from PIL import Image, ImageEnhance, ImageFont, ImageDraw
import io
import emoji

UCLASSIFY_API_KEY = "2SA6uoG0hDtK"
OPENAI_API_KEY = "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"
openai.api_key = OPENAI_API_KEY

def classify_sentiment(text):
    url = "https://api.uclassify.com/v1/uClassify/Sentiment/classify"
    headers= {
        "Authorization": f"Token {UCLASSIFY_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {"texts": [text]}
    response = requests.post(url, headers=headers, json=data)
    result = response.json()
    sentiment = max(result[0]['classification'], key = lambda x: x['p'])['className']
    return sentiment

def generate_image(prompt):
    response = openai.Image.create(
        prompt = prompt,
        n=1,
        size="512x512"
    )

    image_url = response['data'][0]['url']
    image_data=requests.get(image_url).content
    return Image.open(io.BytesIO(image_data))

def enhance_image(img, sentiment):
    enhancer = ImageEnhance.Brightness(img)
    img= enhancer.enhance(1.2 if sentiment == 'positive' else 0.8)

    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.3 if sentiment == "positive" else 0.7)

    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()
    emoji_map = {
        "positive": "😊",
        "negative": "😞",
        "neutral": "😞"
    }

    draw.text((10, 10), emoji.emojize(emoji_map.get(sentiment, "😞")),font=font, fill = "white")
    return img

def run_pipeline(text):
    sentiment = classify_sentiment(text)
    print(f"sentiment: {sentiment}")
    prompt = f"A {sentiment} scene inspired by {text}"
    img = generate_image(prompt)
    enhanced_img = enhance_image(img, sentiment)

    enhanced_img.show()

if __name__ == "__main__":
    user_input = input("enter your text: ")
    run_pipeline(user_input)