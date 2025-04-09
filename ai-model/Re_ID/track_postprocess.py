from collections import Counter
import numpy as np
import cv2
from sklearn.metrics.pairwise import cosine_similarity
from .reid_model import ReIDModel, preprocess

def filter_short_lived_ids(tracks, min_frames=50):
  
    id_counts = Counter()
    for frame_data in tracks["players"]:
        for pid in frame_data.keys():
            id_counts[pid] += 1
    valid_ids = {pid for pid, count in id_counts.items() if count >= min_frames}
    for idx in range(len(tracks["players"])):
        frame_data = tracks["players"][idx]
        filtered = {pid: info for pid, info in frame_data.items() if pid in valid_ids}
        tracks["players"][idx] = filtered

def extract_embedding(frame, bbox, reid_model):
    
    x1, y1, x2, y2 = map(int, bbox)
    crop = frame[y1:y2, x1:x2]
    if crop.size == 0:
       
        return np.zeros(128)
    processed = preprocess(crop)
    embedding = reid_model.extract_embedding(processed)
    return embedding

def reid_merge_tracks(tracks, video_frames, reid_model, threshold=0.7):
  
    track_embeddings = {}

    
    for frame_idx, frame_data in enumerate(tracks["players"]):
        frame = video_frames[frame_idx]
        for pid, info in frame_data.items():
            if pid not in track_embeddings:
                embedding = extract_embedding(frame, info['bbox'], reid_model)
                track_embeddings[pid] = embedding

    
    merge_mapping = {}  
    pids = list(track_embeddings.keys())
    for i in range(len(pids)):
        for j in range(i + 1, len(pids)):
            pid_i = pids[i]
            pid_j = pids[j]
            emb_i = track_embeddings[pid_i].reshape(1, -1)
            emb_j = track_embeddings[pid_j].reshape(1, -1)
            sim = cosine_similarity(emb_i, emb_j)[0][0]
            if sim > threshold:
                
                canonical = min(pid_i, pid_j)
                duplicate = max(pid_i, pid_j)
                merge_mapping[duplicate] = canonical

    
    for idx in range(len(tracks["players"])):
        frame_data = tracks["players"][idx]
        new_frame_data = {}
        for pid, info in frame_data.items():
            canonical_pid = merge_mapping.get(pid, pid)
            new_frame_data[canonical_pid] = info
        tracks["players"][idx] = new_frame_data

def keep_top_22_ids(tracks):
    
    id_counter = Counter()
    for frame_data in tracks["players"]:
        id_counter.update(frame_data.keys())
    top_22_ids = {pid for pid, _ in id_counter.most_common(22)}
    for idx in range(len(tracks["players"])):
        frame_data = tracks["players"][idx]
        tracks["players"][idx] = {pid: info for pid, info in frame_data.items() if pid in top_22_ids}
