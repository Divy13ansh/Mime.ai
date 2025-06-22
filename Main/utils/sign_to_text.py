# import cv2
# from sign_language_translator import get_model

# model = get_model("gesture_mp_base-01")  # load pretrained model
# if model is None:
#     raise ValueError("Model could not be loaded. Please check the path or installation")

# def extract_frames(video_path):
#     cap = cv2.VideoCapture(video_path)
#     frames = []
#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break
#         frames.append(frame)
#     cap.release()
#     return frames

# def sign_video_to_text(video_path: str) -> str:
#     frames = extract_frames(video_path)
#     features = model.extract_features(frames)
#     text = model(features)  # Run translation
#     return text
