import os
import requests

SYSTEM_PROMPT = os.getenv('SYSTEM_PROMPT', 'You are a helpful assistant.')
GITHUB_API_KEY = os.getenv("GITHUB_TOKEN")  # put your GitHub PAT in .env
GITHUB_API_URL = "https://models.inference.ai.azure.com/chat/completions"

def generate_reply(user_text: str) -> str:
    """Call GitHub Models (GPT-4o-mini free tier) and return assistant's reply text."""
    headers = {
        "Authorization": f"Bearer {GITHUB_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-4o-mini",   # free tier model
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_text}
        ],
        "max_tokens": 600,
        "temperature": 0.7,
    }
    response = requests.post(GITHUB_API_URL, headers=headers, json=data)
    response.raise_for_status()
    result = response.json()
    return result["choices"][0]["message"]["content"].strip()
