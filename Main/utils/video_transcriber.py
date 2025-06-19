import ffmpeg
import os
import requests
import time

ASSEMBLYAI_API_KEY = os.getenv("ASSEMBLYAI_API_KEY")  # or hardcode for local testing

def extract_audio_from_video(video_path, audio_output_path):
    ffmpeg.input(video_path).output(audio_output_path, format='mp3', acodec='libmp3lame').run(overwrite_output=True)

def upload_audio_to_assemblyai(audio_path):
    headers = {'authorization': ASSEMBLYAI_API_KEY}
    with open(audio_path, 'rb') as f:
        response = requests.post('https://api.assemblyai.com/v2/upload', headers=headers, data=f)
    response.raise_for_status()
    return response.json()['upload_url']

def transcribe_audio_assemblyai(audio_url):
    headers = {
        "authorization": ASSEMBLYAI_API_KEY,
        "content-type": "application/json"
    }
    transcript_request = {"audio_url": audio_url}
    response = requests.post("https://api.assemblyai.com/v2/transcript", json=transcript_request, headers=headers)
    response.raise_for_status()
    transcript_id = response.json()['id']

    # Polling
    while True:
        polling_response = requests.get(f"https://api.assemblyai.com/v2/transcript/{transcript_id}", headers=headers)
        result = polling_response.json()
        if result['status'] == 'completed':
            return result['text']
        elif result['status'] == 'error':
            raise Exception(result['error'])
        time.sleep(3)

def video_to_text(video_path):
    audio_path = video_path.replace(".mp4", ".mp3").replace(".mov", ".mp3")
    extract_audio_from_video(video_path, audio_path)
    upload_url = upload_audio_to_assemblyai(audio_path)
    text = transcribe_audio_assemblyai(upload_url)
    os.remove(audio_path)
    return text
