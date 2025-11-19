import requests
import json

from environs import Env

env = Env()
env.read_env()

api_key=env.str("VOICE")

def tts(text):
    url = 'https://uzbekvoice.ai/api/v1/tts'
    headers = {
        'Authorization': api_key,
        'Content-Type': 'application/json'
    }
    data = {
        'text': text,
        'model': "lola",
        'blocking': "true",
        'webhook_notification_url': "https://example.com"
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            return response.json()['result']['url']
        else:
            return f"Request failed with status code {response.status_code}: {response.text}"
    except requests.exceptions.Timeout:
        return "Request timed out. The API response took too long to arrive."


