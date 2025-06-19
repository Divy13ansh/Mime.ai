import json
import csv
import pandas as pd

# === Input and output ===
INPUT_JSON = "static/json/reference1_normalized.json"
OUTPUT_CSV = "reference1_normalized.csv"

# === Load the reference JSON ===
with open(INPUT_JSON, "r") as f:
    data = json.load(f)

rows = []

# === Process each gloss ===
for gloss, frames in data.items():
    for frame_data in frames:
        frame_number = frame_data["Frame"]

        for hand in ["Left", "Right"]:
            hand_coords = frame_data.get(f"{hand} Hand Coordinates", [])
            for joint in hand_coords:
                row = {
                    "Gloss": gloss,
                    "Frame": frame_number,
                    "Hand": hand,
                    "Joint Index": joint["Joint Index"],
                    "X": joint["Coordinates"][0],
                    "Y": joint["Coordinates"][1],
                    "Z": joint["Coordinates"][2]
                }
                rows.append(row)

df = pd.DataFrame(rows)
df.to_csv(OUTPUT_CSV, index=False)
print(f"✅ Saved flattened data to {OUTPUT_CSV}")
