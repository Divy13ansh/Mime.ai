import json

REFERENCE_FILE = "static/json/reference1.json"
OUTPUT_FILE = "words.txt"

# Load reference data
with open(REFERENCE_FILE, "r") as f:
    reference_data = json.load(f)

# Extract top-level keys (gloss words)
words = sorted(reference_data.keys())

# Save to file
with open(OUTPUT_FILE, "w") as out:
    for word in words:
        out.write(f"{word}\n")

print(f"✅ Saved {len(words)} words to '{OUTPUT_FILE}'")
