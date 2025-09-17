import os
import tempfile
import uuid
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from .services.stt import transcribe
from .services.llm import generate_reply
from .services.tts import synthesize

def index(request):
    return render(request, 'voiceapp/index.html')


@csrf_exempt
@require_POST
def voice_interact(request):
    audio_file = request.FILES.get('audio')
    if not audio_file:
        return JsonResponse({'error': 'no audio file provided (field name: audio)'}, status=400)

    suffix = os.path.splitext(audio_file.name)[1] or '.wav'
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    try:
        for chunk in audio_file.chunks():
            tmp.write(chunk)
    finally:
        tmp.close()

    # STT - text
    transcript = transcribe(tmp.name) # path of the audio file stored in the temporary directory

    # LLM - reply
    reply_text = generate_reply(transcript)

    # TTS - save audio file
    out_dir = os.path.join(settings.MEDIA_ROOT, 'voice_outputs') # media/voice_outputs
    os.makedirs(out_dir, exist_ok=True) # create the directory if it doesn't exist
    out_filename = f"response_{uuid.uuid4().hex}.mp3"
    out_path = os.path.join(out_dir, out_filename)
    synthesize(reply_text, out_path) # tts

    audio_url = request.build_absolute_uri(settings.MEDIA_URL + f"voice_outputs/{out_filename}")

    return JsonResponse({
        'transcript': transcript,
        'response': reply_text,
        'audio_url': audio_url,
    })



