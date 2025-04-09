import pickle
import cv2
import numpy as np
import os
import sys
sys.path.append('../')
from utils.bbox_utils import measure_distance, measure_xy_distance, get_center_of_bbox, get_foot_position

class CameraMovementEstimator:
    def __init__(self, frame: np.ndarray) -> None:
        self.minimum_distance = 5
        self.lk_params = dict(
            winSize=(15, 15),
            maxLevel=2,
            criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03)
        )
        first_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        mask_features = np.zeros_like(first_gray)
        mask_features[:, 0:20] = 1
        mask_features[:, 900:1050] = 1

        self.features = dict(
            maxCorners=100,
            qualityLevel=0.3,
            minDistance=3,
            blockSize=7,
            mask=mask_features
        )

    def add_adjust_positions_to_tracks(self, tracks: dict, camera_movement_per_frame: list) -> None:
        
        from utils.bbox_utils import get_center_of_bbox, get_foot_position
        for category, frame_list in tracks.items():
            for fnum, track_dict in enumerate(frame_list):
                dx, dy = camera_movement_per_frame[fnum]
                for t_id, info in track_dict.items():
                    if 'position' not in info:
                        bbox = info.get("bbox")
                        if not bbox:
                            continue
                        if category == 'ball':
                            pos = get_center_of_bbox(bbox)
                        else:
                            pos = get_foot_position(bbox)
                        info['position'] = pos
                    px, py = info['position']
                    info['position_adjusted'] = (px - dx, py - dy)

    def get_camera_movement(self, frames: list, read_from_stub: bool = False, stub_path: str = None) -> list:
        
        if read_from_stub and stub_path and os.path.exists(stub_path):
            try:
                with open(stub_path, 'rb') as f:
                    return pickle.load(f)
            except Exception as e:
                print(f"[WARN] Could not load camera stub: {e}")

        n_frames = len(frames)
        camera_movement = [[0, 0] for _ in range(n_frames)]
        old_gray = cv2.cvtColor(frames[0], cv2.COLOR_BGR2GRAY)
        old_features = cv2.goodFeaturesToTrack(old_gray, **self.features)

        for fidx in range(1, n_frames):
            frame_gray = cv2.cvtColor(frames[fidx], cv2.COLOR_BGR2GRAY)
            new_features, status, _ = cv2.calcOpticalFlowPyrLK(
                old_gray, frame_gray, old_features, None, **self.lk_params
            )
            max_dist = 0
            cam_dx, cam_dy = 0, 0
            if new_features is not None and status is not None:
                for (n_pt, o_pt, st) in zip(new_features, old_features, status):
                    if st == 1:
                        np_new = n_pt.ravel()
                        np_old = o_pt.ravel()
                        dist = ((np_new[0]-np_old[0])**2 + (np_new[1]-np_old[1])**2) ** 0.5
                        if dist > max_dist:
                            max_dist = dist
                            dx = np_old[0] - np_new[0]
                            dy = np_old[1] - np_new[1]
                            cam_dx, cam_dy = dx, dy

            if max_dist > self.minimum_distance:
                camera_movement[fidx] = [cam_dx, cam_dy]
                new_good = cv2.goodFeaturesToTrack(frame_gray, **self.features)
                if new_good is not None:
                    old_features = new_good
            old_gray = frame_gray.copy()

        if stub_path:
            try:
                with open(stub_path, 'wb') as f:
                    pickle.dump(camera_movement, f)
            except Exception as e:
                print(f"[WARN] Could not save camera stub: {e}")

        return camera_movement

    def draw_camera_movement(self, frames: list, camera_movement_per_frame: list) -> list:
       
        output_frames = []
        for idx, frm in enumerate(frames):
            fcopy = frm.copy()
            overlay = fcopy.copy()
            cv2.rectangle(overlay, (0, 0), (500, 100), (255, 255, 255), -1)
            alpha = 0.6
            cv2.addWeighted(overlay, alpha, fcopy, 1 - alpha, 0, fcopy)
            dx, dy = camera_movement_per_frame[idx]
            cv2.putText(fcopy, f"Camera Movement X: {dx:.2f}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 3)
            cv2.putText(fcopy, f"Camera Movement Y: {dy:.2f}", (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 3)
            output_frames.append(fcopy)
        return output_frames
