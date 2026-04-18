import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("STABILITY_API_KEY")

def generate_image(prompt):
    url = "https://api.stability.ai/v2beta/stable-image/generate/core"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Accept": "image/*"
    }

    files = {
        "prompt": (None, prompt),
        "output_format": (None, "png")
    }

    response = requests.post(url, headers=headers, files=files)

    if response.status_code != 200:
        raise Exception(response.text)

    return response.content