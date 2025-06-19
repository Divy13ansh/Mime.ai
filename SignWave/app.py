from flask import Flask, render_template, request, jsonify
import json
import re
import os
import nltk
from nltk.stem import WordNetLemmatizer

nltk.download('wordnet')

app = Flask(__name__)

# Load reference data
REFERENCE_FILE = "static/json/reference1_normalized.json"
with open(REFERENCE_FILE, "r") as f:
    reference_data = json.load(f)

# Gloss simplifier
lemmatizer = WordNetLemmatizer()
STOPWORDS = {"a", "an", "the", "is", "am", "are", "was", "were", "be", "do", "does", "did", "can", "to", "for", "with", "on", "in", "at", "from", "of"}

def english_to_gloss(text):
    words = re.findall(r'\b\w+\b', text.lower())
    gloss = [lemmatizer.lemmatize(w) for w in words if w not in STOPWORDS]
    return gloss

def modify_words(text):
    gloss_words = english_to_gloss(text)
    matched_words = [word for word in gloss_words if word in reference_data]
    return ' '.join(matched_words)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload_file", methods=["POST"])
def upload_file():
    rawText = request.form["text"]
    modText = modify_words(rawText)
    print("🔊 Raw:", rawText)
    print("🧠 Gloss:", english_to_gloss(rawText))
    print("✅ Final words used:", modText)
    return jsonify({"result": modText})

if __name__ == '__main__':
    app.run(debug=True)
