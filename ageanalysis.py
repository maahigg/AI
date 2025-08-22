import requests

UCLASSIFY_API_KEY = "2SA6uoG0hDtK"

def estimate_age(text):
    url = "https://api.uclassify.com/v1/uClassify/ageanalyzer/classify"
    headers={
        "Authorization": f"Token {UCLASSIFY_API_KEY}",
        "Content-Type": "application/json"
    }

    