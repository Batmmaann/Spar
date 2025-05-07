import os
import pickle
import numpy as np
import pandas as pd
import cv2
from typing import List, Dict, Any, Optional
from ultralytics import YOLO
import supervision as sv
from deep_sort_realtime.deepsort_tracker import DeepSort

def clamp_bbox(bbox: List[float], frame_width: int, frame_height: int) -> List[float]:
    x1, y1, x2, y2 = bbox
    x1 = max(0, min(x1, frame_width - 1))
    y1 = max(0, min(y1, frame_height - 1))
    x2 = max(0, min(x2, frame_width - 1))
    y2 = max(0, min(y2, frame_height - 1))
    return [x1, y1, x2, y2]

class DeepSortTracker:

    def __init__(self, model_path: str, device: str = 'cuda') -> None:
        self.model = YOLO(model_path)
        self.device = device
        self.deepsort = DeepSort(
            max_iou_distance=0.7,
            max_cosine_distance=0.4,
            max_age=30,
            n_init=3
        )

    def detect_frames(self, frames: List[np.ndarray]) -> List[Any]:
        batch_size = 20
        detections = []
        for i in range(0, len(frames), batch_size):
            batch = frames[i: i + batch_size]
            results = self.model.predict(batch, conf=0.1, device=self.device)
            detections.extend(results)
        return detections

    def get_object_tracks(
        self,
        frames: List[np.ndarray],
        read_from_stub: bool = False,
        stub_path: Optional[str] = None
    ) -> Dict[str, List[Dict[Any, Any]]]:
        if read_from_stub and stub_path and os.path.exists(stub_path):
            try:
                with open(stub_path, 'rb') as f:
                    return pickle.load(f)
            except Exception as e:
                print(f"Error loading stub from {stub_path}: {e}")

        tracks = {"players": [], "referees": [], "ball": []}
        detections = self.detect_frames(frames)
        frame_h, frame_w = frames[0].shape[:2]

        for frame_idx, detection in enumerate(detections):
            # extract raw YOLO outputs as numpy arrays
            raw_bboxes = detection.boxes.xyxy.cpu().numpy()    # shape (N,4)
            raw_confs  = detection.boxes.conf.cpu().numpy()    # shape (N,)
            raw_cls    = detection.boxes.cls.cpu().numpy()     # shape (N,)

            ds_input = []
            for det_idx, raw in enumerate(raw_bboxes):
                clamped = clamp_bbox(raw.tolist(), frame_w, frame_h)
                ds_input.append([clamped, float(raw_confs[det_idx]), int(raw_cls[det_idx])])

            outputs = self.deepsort.update_tracks(ds_input, frame=frames[frame_idx])
            frame_tracks = {"players": {}, "referees": {}, "ball": {}}

            for t in outputs:
                if not t.is_confirmed() or t.time_since_update > 1:
                    continue

                ds_box = clamp_bbox(t.to_tlbr().tolist(), frame_w, frame_h)
                det_idx = getattr(t, 'det_index', None)
                raw_box = ds_input[det_idx][0] if det_idx is not None else ds_box

                tid = t.track_id
                cls = t.det_class

                entry = {"bbox": ds_box, "det_bbox": raw_box}

                if cls == 0:
                    frame_tracks["ball"][1] = entry
                elif cls in [1, 2]:
                    frame_tracks["players"][tid] = entry
                elif cls == 3:
                    frame_tracks["referees"][tid] = entry

            tracks["players"].append(frame_tracks["players"])
            tracks["referees"].append(frame_tracks["referees"])
            tracks["ball"].append(frame_tracks["ball"])

        if stub_path:
            try:
                with open(stub_path, 'wb') as f:
                    pickle.dump(tracks, f)
            except Exception as e:
                print(f"Error saving stub to {stub_path}: {e}")

        return tracks

    def add_position_to_tracks(self, tracks: Dict[str, List[Dict[Any, Any]]]) -> None:
        from utils.bbox_utils import get_center_of_bbox, get_foot_position
        for cat, frames in tracks.items():
            for frame in frames:
                for tid, info in frame.items():
                    bbox = info.get("bbox")
                    if not bbox: continue
                    if cat == 'ball':
                        info['position'] = get_center_of_bbox(bbox)
                    else:
                        info['position'] = get_foot_position(bbox)

    def interpolate_ball_positions(self, ball_positions: List[Dict[Any, Any]]) -> List[Dict[Any, Any]]:        
        bboxes = [f.get(1, {}).get('bbox', [0,0,0,0]) for f in ball_positions]
        df = pd.DataFrame(bboxes, columns=['x1','y1','x2','y2'])
        df = df.interpolate().bfill().ffill()
        return [{1: {"bbox": row.tolist()}} for _, row in df.iterrows()]
