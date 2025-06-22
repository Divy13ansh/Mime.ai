# import spacy
# import re
from django.conf import settings
import requests

# Load spaCy's small English model
# nlp = spacy.load("en_core_web_sm")

# Load your ASL vocabulary set
with open('Main/vocab/animation_words.txt', 'r') as f:
    animation_words = [line.strip().lower() for line in f if line.strip()]

word_list = ", ".join(animation_words)

def get_synonym_in_vocab_spacy(word):
    
    word = word.lower()

    if word in animation_words:
        return word
    
    else:
        # Use OpenRouter API to find the closest word in the vocabulary
        prompt = f"""
        You are an AI that helps translate text into sign language. You are given:

        - An input word: "{word}"
        - A list of known words that can be animated: {animation_words}

        Your task:
        - If the input word is in the list, return it.
        - If a **close synonym** is in the list (e.g., "father" → "dad"), return it.
        - If **no close synonym** exists, return "-1"

        ⚠️ Do not guess. If you are unsure or the match is too weak, return "-1".
        Only return the chosen word or "-1". No explanation.
        """


        headers = {
                "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "http://localhost",
                "X-Title": "Mime AI Glossifier",
                "X-User": "MimeAIUser"
            }

        payload = {
            "model": "x-ai/grok-3-mini",  # Switched to a more capable model
            "temperature": 0.7,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 6000  # Increased to ensure complete responses
        }

        print(f"Requesting synonym for: {word}")
        print(f"Payload: {payload}")

        # Make the API request
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        print(f"Response: {data}")
        return data['choices'][0]['message']['content'].strip() if 'choices' in data and data['choices'] else None

def normalize_and_glossify(text):
    # Clean text
    text = text.lower()
    
    gloss = []
    for token in text.split():
        if token in animation_words:
            gloss.append(token)
        else:
            # Fallback: return token itself or "[UNK]"
            s = get_synonym_in_vocab_spacy(token)
            if s != "-1":
                gloss.append(s)
            else:
                gloss.append(token)  # or "[UNK]" if you prefer

    return gloss
