import json

with open("static/json/reference1.json") as f:
    data = json.load(f)

valid_words = []

for word, frames in data.items():
    usable = any(
        f["Left Hand Coordinates"] or f["Right Hand Coordinates"]
        for f in frames
    )
    if usable:
        valid_words.append(word)

print(f"✅ {len(valid_words)} usable words found")
print(valid_words)
