# mime_ai/Main/utils/assemblyai_transcriber.py

import requests
import time
import os
from dotenv import load_dotenv
load_dotenv()

ASSEMBLYAI_API_KEY = os.getenv("ASSEMBLYAI_API_KEY")
print(ASSEMBLYAI_API_KEY)

upload_endpoint = "https://api.assemblyai.com/v2/upload"
transcript_endpoint = "https://api.assemblyai.com/v2/transcript"

headers = {
    "authorization": ASSEMBLYAI_API_KEY,
    "content-type": "application/json"
}

def upload_audio(file_path):
    with open(file_path, 'rb') as f:
        response = requests.post(upload_endpoint, headers={"authorization": ASSEMBLYAI_API_KEY}, files={"file": f})
    response.raise_for_status()
    return response.json()['upload_url']

def transcribe_audio(file_path):
    upload_url = upload_audio(file_path)

    transcript_request = {
        "audio_url": upload_url
    }

    transcript_response = requests.post(transcript_endpoint, json=transcript_request, headers=headers)
    transcript_id = transcript_response.json()['id']

    # Polling until transcription is complete
    while True:
        polling_response = requests.get(f"{transcript_endpoint}/{transcript_id}", headers=headers)
        status = polling_response.json()['status']

        if status == 'completed':
            return polling_response.json()['text']
        elif status == 'error':
            raise Exception(f"Transcription failed: {polling_response.json()['error']}")
        
        time.sleep(3)  # wait before polling again
