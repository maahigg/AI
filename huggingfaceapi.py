import requests

api_url = "https://api-inference.huggingface.co/models/distilbert-base-uncased-finetuned-sst-2-english"

headers = {
    "Authorization": "Bearer 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"
}

text = "i love learning about ai it is so fascinating"

response = requests.post(api_url, headers=headers, json={"inputs": text})
if response.status_code == 200:
    classification = response.json()
    print("predicted label: ", classification[0]['label'])
else:
    print(f"error: {response.status_code}")

import requests

api_url = "https://api-inference.huggingface.co/models/distilbert-base-uncased-finetuned-sst-2-english"

headers = {
    "Authorization": "Bearer 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"
}

text = "i love learning about ai it is so fascinating"

response = requests.post(api_url, headers=headers, json={"inputs": text})
if response.status_code == 200:
    classification = response.json()
    print("predicted label: ", classification[0]['label'])
else:
    print(f"error: {response.status_code}")
