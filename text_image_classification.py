import requests
from PIL import Image, ImageDraw

UCLASSIFY_API_KEY = "2SA6uoG0hDtK"
CLASSIFIER_URL = "https://api.uclassify.com/v1/uClassify/Sentiment/classify"

def classify_text(text):
    headers= {
        "Authorization": f"Token {UCLASSIFY_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {"texts": [text]}
    response = requests.post(CLASSIFIER_URL, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()[0]["classification"]
    else:
        print("api error")
        return None
    
def create_image(classification, output_path = "sentiment_result.jpg"):
    img = Image.new("RGB", (400, 200), color="white")
    draw = ImageDraw.Draw(img)
    y=20
    for item in classification:
        label = item["className"]
        confidence = item["p"]
        draw.text((10, y), f"{label}: {confidence:.2f}", fill="black")
        y+=40
    img.save(output_path)
    print(f"image saved to {output_path}")

def main():
    text = input("enter text to classify").strip()
    if not text:
        print("no input provided")
        return
    
    classification = classify_text(text)
    if classification:
        for item in classification:
            print(f"{item['className']}: {item['p']:.2f}")
        create_image(classification)

if __name__ == "__main__":
    main()