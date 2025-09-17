import os
import requests

ELEVEN_API_KEY = os.getenv('ELEVENLABS_API_KEY') or os.getenv('ELEVEN_API_KEY')

def transcribe(file_path: str) -> str:
    """Simple wrapper around ElevenLabs Speech-to-Text convert endpoint.

    Uses the `scribe_v1` model by default and returns the `text` field.
    """
    url = 'https://api.elevenlabs.io/v1/speech-to-text'
    headers = {'xi-api-key': ELEVEN_API_KEY}
    with open(file_path, 'rb') as f:
        files = {'file': f}
        data = {'model_id': 'scribe_v1'}
        resp = requests.post(url, headers=headers, files=files, data=data)
        resp.raise_for_status()
        j = resp.json()
        # The typical response contains a top-level `text` field
        return j.get('text') or j.get('transcript') or ''