from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import tempfile, os

from .utils.glossifier import normalize_and_glossify
from .utils.assemblyai_transcriber import transcribe_audio
from .utils.video_transcriber import video_to_text
from .utils.translator import translate_to_english

class UnifiedGlossView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        category = request.data.get('category')
        text = request.data.get('text', '')
        file = request.FILES.get('file', None)

        if not category:
            return Response({"error": "Missing category."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            if category == "text":
                if not text:
                    return Response({"error": "Text is required."}, status=status.HTTP_400_BAD_REQUEST)
                gloss = normalize_and_glossify(text)
                return Response({"text": text, "gloss": gloss})

            elif category == "audio":
                if not file:
                    return Response({"error": "Audio file required."}, status=status.HTTP_400_BAD_REQUEST)
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp:
                    for chunk in file.chunks():
                        temp.write(chunk)
                    temp_path = temp.name
                text = transcribe_audio(temp_path)
                os.remove(temp_path)
                gloss = normalize_and_glossify(text)
                return Response({"text": text, "gloss": gloss})

            elif category == "video":
                if not file:
                    return Response({"error": "Video file required."}, status=status.HTTP_400_BAD_REQUEST)
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp:
                    for chunk in file.chunks():
                        temp.write(chunk)
                    temp_path = temp.name
                text = video_to_text(temp_path)
                os.remove(temp_path)
                gloss = normalize_and_glossify(text)
                return Response({"text": text, "gloss": gloss})

            elif category == "translate":
                if not text:
                    return Response({"error": "Text is required for translation."}, status=status.HTTP_400_BAD_REQUEST)
                english_text = translate_to_english(text)
                gloss = normalize_and_glossify(english_text)
                return Response({
                    "original": text,
                    "translated": english_text,
                    "gloss": gloss
                })

            else:
                return Response({"error": f"Unsupported category '{category}'"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class Ping(APIView):
    def get(self, request):
        ping = {'message': "pong"}
        return Response(ping)