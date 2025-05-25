import os
import requests
from dotenv import load_dotenv

load_dotenv() 

YANDEX_API_KEY = os.getenv("YANDEX_API_KEY")
YANDEX_FOLDER_ID = os.getenv("YANDEX_FOLDER_ID")

def ask_yandex_gpt(prompt: str) -> str:
    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"

    headers = {
        "Authorization": f"Api-Key {YANDEX_API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "modelUri": f"gpt://{YANDEX_FOLDER_ID}/yandexgpt-lite",
        "completionOptions": {
            "stream": False,
            "temperature": 0.7,
            "maxTokens": 500
        },
        "messages": [
            {"role": "system", "text": "Ты модный стилист. Отвечай кратко, уверенно и со вкусом."},
            {"role": "user", "text": prompt}
        ]
    }

    response = requests.post(url, headers=headers, json=body)

    if response.status_code == 200:
        return response.json()["result"]["alternatives"][0]["message"]["text"]
    else:
        return f"⚠️ Ошибка: {response.status_code} — {response.text}"