from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from .utils.glossifier import normalize_and_glossify
from .utils.video_transcriber import video_to_text
from .utils.sign_to_text import sign_video_to_text
from Main.utils.assemblyai_transcriber import transcribe_audio
from Main.utils.translator import translate_to_english
import tempfile
import os

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
    def post(self, request, *args, **kwargs):
        video_file = request.FILES.get('video')
        if not video_file:
            return Response({"error": "No video file provided."}, status=status.HTTP_400_BAD_REQUEST)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
            for chunk in video_file.chunks():
                temp_file.write(chunk)
            temp_file_path = temp_file.name

        try:
            text = video_to_text(temp_file_path)
            gloss = normalize_and_glossify(text)
            return Response({"text": text, "gloss": gloss}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class TranslateToGlossView(APIView):
    def post(self, request):
        input_text = request.data.get("text", "")
        if not input_text:
            return Response({"error": "Text is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            english_text = translate_to_english(input_text)
            gloss_text = normalize_and_glossify(english_text)
            return Response({
                "original": input_text,
                "translated": english_text,
                "gloss": gloss_text
            })
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
# class SignVideoToTextView(APIView):
#     parser_classes = [MultiPartParser]

#     def post(self, request):
#         video_file = request.FILES.get('video')
#         if not video_file:
#             return Response({"error": "No video uploaded."}, 400)

#         with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
#             video_file.chunks()
#             for chunk in video_file.chunks():
#                 tmp.write(chunk)
#             video_path = tmp.name

#         try:
#             sentence = sign_video_to_text(video_path)
#             return Response({"text": sentence}, 200)
#         except Exception as e:
#             return Response({"error": str(e)}, 500)
