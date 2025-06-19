import os
import json
import cv2
import mediapipe as mp

# === Config ===
ARCHIVE_BASE = "../archive"
VIDEO_DIR = os.path.join(ARCHIVE_BASE, "videos")
METADATA_FILE = os.path.join(ARCHIVE_BASE, "WLASL_v0.3.json")
OUTPUT_FILE = "static/json/reference1.json"  # ✅ Final file for full dataset
MAX_FRAMES_PER_VIDEO = 20
MAX_GLOSSES = 999999  # No cap — do all glosses

# === MediaPipe Setup ===
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# === Load Metadata ===
with open(METADATA_FILE, "r") as f:
    metadata = json.load(f)

reference_data = {}
gloss_count = 0
processed_videos = set()

# === Process Glosses ===
for entry in metadata:
    gloss = entry["gloss"].lower().strip()
    if gloss in reference_data:
        continue
    if gloss_count >= MAX_GLOSSES:
        break

    for inst in entry["instances"]:
        video_id = str(inst["video_id"]).zfill(5)
        video_path = os.path.join(VIDEO_DIR, f"{video_id}.mp4")
        if not os.path.exists(video_path):
            continue
        if video_id in processed_videos:
            continue

        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            continue

        print(f"🎬 {gloss}: {video_id}.mp4")
        frame_id = 0
        processed_videos.add(video_id)
        reference_data[gloss] = []

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret or frame_id >= MAX_FRAMES_PER_VIDEO:
                break

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(rgb)

            frame_data = {
                "Frame": frame_id,
                "Left Hand Coordinates": [],
                "Right Hand Coordinates": []
            }

            if results.multi_hand_landmarks and results.multi_handedness:
                for idx, handedness in enumerate(results.multi_handedness):
                    label = handedness.classification[0].label
                    landmarks = results.multi_hand_landmarks[idx].landmark
                    if len(landmarks) == 21:
                        joints = [
                            {"Joint Index": i, "Coordinates": [lm.x, lm.y, lm.z]}
                            for i, lm in enumerate(landmarks)
                        ]
                        if label == "Left":
                            frame_data["Left Hand Coordinates"] = joints
                        else:
                            frame_data["Right Hand Coordinates"] = joints

            if (
                len(frame_data["Left Hand Coordinates"]) == 21 or
                len(frame_data["Right Hand Coordinates"]) == 21
            ):
                reference_data[gloss].append(frame_data)

            frame_id += 1

        cap.release()
        gloss_count += 1
        break  # ✅ Only 1 video per gloss

# === Save Cleaned Output ===
cleaned_data = {g: f for g, f in reference_data.items() if f}
os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

with open(OUTPUT_FILE, "w") as f:
    json.dump(cleaned_data, f, indent=2)

hands.close()
print(f"\n✅ Saved {len(cleaned_data)} glosses to {OUTPUT_FILE}")
