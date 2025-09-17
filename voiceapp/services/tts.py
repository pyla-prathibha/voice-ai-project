import os
import requests

ELEVEN_API_KEY = os.getenv('ELEVENLABS_API_KEY') or os.getenv('ELEVEN_API_KEY')
VOICE_ID = os.getenv('ELEVEN_VOICE_ID', 'YOUR_DEFAULT_VOICE_ID')

def synthesize(text: str, out_path: str) -> str:
    """Call ElevenLabs Text-to-Speech and write MP3 to out_path.

    This uses the HTTP Create Speech endpoint which returns audio data.
    """
    url = f'https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}'
    headers = {
        'xi-api-key': ELEVEN_API_KEY,
        'Content-Type': 'application/json',
        'Accept': 'audio/mpeg',
    }
    payload = {
        'text': text,
        # optional voice settings
        'voice_settings': {
            'stability': 0.5,
            'similarity_boost': 0.75,
        }
    }
    resp = requests.post(url, headers=headers, json=payload, stream=True)
    resp.raise_for_status()
    with open(out_path, 'wb') as f:
        for chunk in resp.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
    return out_path