import cv2
import os
from skimage.metrics import structural_similarity as ssim
import numpy as np

def extract_frames_by_difference(video_path, output_dir="generated/temp_frames", threshold=25):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return []

    image_paths = []
    prev_frame = None
    frame_count = 0
    saved_frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray_frame = cv2.GaussianBlur(gray_frame, (21, 21), 0)

        if prev_frame is None:
            prev_frame = gray_frame
            # Save the first frame
            image_path = os.path.join(output_dir, f"frame_{frame_count}.jpg")
            cv2.imwrite(image_path, frame)
            image_paths.append(image_path)
            saved_frame_count += 1
            continue

        frame_delta = cv2.absdiff(prev_frame, gray_frame)
        thresh = cv2.threshold(frame_delta, threshold, 255, cv2.THRESH_BINARY)[1]
        
        thresh = cv2.dilate(thresh, None, iterations=2)
        
        if np.count_nonzero(thresh) > 0:
            image_path = os.path.join(output_dir, f"frame_{frame_count}.jpg")
            cv2.imwrite(image_path, frame)
            image_paths.append(image_path)
            saved_frame_count += 1

        prev_frame = gray_frame

    cap.release()
    print(f"Processed {frame_count} frames and saved {saved_frame_count} frames.")
    return image_paths

def extract_key_frames(video_path, output_dir="generated/temp_frames", ssim_threshold=0.70, cooldown_frames=5):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return []

    image_paths = []
    prev_frame = None
    frame_count = 0
    saved_frame_count = 0
    cooldown_counter = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1

        if cooldown_counter > 0:
            cooldown_counter -= 1
            prev_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            continue

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if prev_frame is None:
            prev_frame = gray_frame
            # Save the first frame
            image_path = os.path.join(output_dir, f"frame_{frame_count}.jpg")
            cv2.imwrite(image_path, frame)
            image_paths.append(image_path)
            saved_frame_count += 1
            continue

        # Resize frames for faster comparison
        resized_prev_frame = cv2.resize(prev_frame, (256, 144))
        resized_gray_frame = cv2.resize(gray_frame, (256, 144))
        
        score, _ = ssim(resized_prev_frame, resized_gray_frame, full=True)

        if score < ssim_threshold:
            image_path = os.path.join(output_dir, f"frame_{frame_count}.jpg")
            cv2.imwrite(image_path, frame)
            image_paths.append(image_path)
            saved_frame_count += 1
            cooldown_counter = cooldown_frames

        prev_frame = gray_frame

    cap.release()
    print(f"Processed {frame_count} frames and saved {saved_frame_count} key frames.")
    return image_paths