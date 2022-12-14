import requests
import json
from dotenv import load_dotenv
import os

load_dotenv("./.env")


def openai_text_gen(prompt):
    url = "https://api.openai.com/v1/completions"

    payload = json.dumps(
        {
            "model": "text-davinci-003",
            "prompt": f"{prompt}",
            "max_tokens": 4000,
            "temperature": 1,
        }
    )
    headers = {
        "origin": "https://chat.openai.com",
        "referer": "https://chat.openai.com/chat",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
        "Authorization": os.getenv("TEXT_GENERATE_TOKEN"),
        "Content-Type": "application/json",
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.content)
    data = response.json().get("choices")
    if data:
        text = data[0]["text"]
    else:
        text = "Not able to generate text :("
    return text


if __name__ == "__main__":
    print(openai_text_gen("generate a promt for a dog sitting on a horse"))
