from googletrans import Translator

translator = Translator()

def translate_to_english(text):
    result = translator.translate(text, dest='en')
    return result.text
