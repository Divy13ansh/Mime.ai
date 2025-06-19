from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from .utils.glossifier import normalize_and_glossify
from Main.utils.assemblyai_transcriber import transcribe_audio
import tempfile
import os
from moviepy.editor import VideoFileClip

class TextToGlossView(APIView):
    def post(self, request):
        input_text = request.data.get("text", "")
        if not input_text:
            return Response({"error": "Text input required"}, status=status.HTTP_400_BAD_REQUEST)
        
        gloss = normalize_and_glossify(input_text)
        return Response({"gloss": gloss}, status=status.HTTP_200_OK)
    
class AudioToGlossView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        if 'audio' not in request.FILES:
            return Response({'error': 'Audio file missing'}, status=status.HTTP_400_BAD_REQUEST)

        audio_file = request.FILES['audio']
        
        # Save uploaded file to temp location
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
            for chunk in audio_file.chunks():
                temp_file.write(chunk)
            temp_file_path = temp_file.name

        try:
            # Transcribe using whisper
            text = transcribe_audio(temp_file_path)

            # Clean and glossify
            gloss = normalize_and_glossify(text)

            return Response({
                "text": text,
                "gloss": gloss
            }, status=status.HTTP_200_OK)
        finally:
            # Clean up temp file
            os.remove(temp_file_path)

class VideoToGlossView(APIView):
    def post(self, request):
        video_file = request.FILES.get("video")
        if not video_file:
            return Response({"error": "No video file provided."}, status=400)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video:
            temp_video.write(video_file.read())
            temp_video_path = temp_video.name

        try:
            # Extract audio
            video_clip = VideoFileClip(temp_video_path)
            temp_audio_path = temp_video_path.replace(".mp4", ".mp3")
            video_clip.audio.write_audiofile(temp_audio_path, codec='libmp3lame')

            # Transcribe
            text = transcribe_audio(temp_audio_path)

            # Glossify
            glossified = normalize_and_glossify(text)

            # Clean up
            os.remove(temp_video_path)
            os.remove(temp_audio_path)

            return Response({"input": text, "glossified": glossified}, status=200)

        except Exception as e:
            return Response({"error": str(e)}, status=500)
