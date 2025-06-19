import spacy
import re

# Load spaCy's small English model
nlp = spacy.load("en_core_web_sm")

# Load your ASL vocabulary set
with open('Main/vocab/animation_words.txt', 'r') as f:
    animation_words = set(word.strip().lower() for word in f.readlines())

def get_synonym_in_vocab_spacy(word):
    # Optional: Basic synonym fallback using simple rule (spaCy doesn't provide WordNet directly)
    # You can later integrate a synonym dictionary here manually or via WordNet API
    return None

def normalize_and_glossify(text):
    # Clean text
    text = re.sub(r'[^a-zA-Z\s]', '', text).lower()
    
    # Use spaCy to process the text
    doc = nlp(text)
    
    gloss = []
    for token in doc:
        lemma = token.lemma_.lower()
        if lemma in animation_words:
            gloss.append(lemma)
        else:
            # Fallback: return token itself or "[UNK]"
            # gloss.append("[UNK]")
            continue
    
    return gloss
