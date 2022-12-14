import requests
import json
from dotenv import load_dotenv
import os

load_dotenv("./.env")


def openai_image_gen(prompt):
    url = "https://api.openai.com/v1/images/generations"

    payload = json.dumps({"prompt": f"{prompt}", "n": 1, "size": "1024x1024"})
    headers = {
        "Content-Type": "application/json",
        "Authorization": os.getenv("IMAGE_GENERATE_TOKEN"),
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    data = response.json().get("data")
    if data:
        url = data[0].get("url")
    else:
        url = "https://upload.wikimedia.org/wikipedia/commons/e/e7/"
        "Everest_North_Face_toward_Base_Camp_Tibet_Luca_Galuzzi_2006.jpg"
    return url


if __name__ == "__main__":
    print(openai_image_gen("a dog sitting on a horse"))
