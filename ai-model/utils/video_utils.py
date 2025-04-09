import cv2
from typing import List
import numpy as np

def read_video(video_path: str) -> list:
    cap = cv2.VideoCapture(video_path)
    frames = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
    cap.release()
    return frames

def save_video(output_frames: list, output_path: str) -> None:
    if not output_frames:
        print("No frames to save.")
        return
    height, width = output_frames[0].shape[:2]
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_path, fourcc, 24, (width, height))
    for frame in output_frames:
        out.write(frame)
    out.release()
