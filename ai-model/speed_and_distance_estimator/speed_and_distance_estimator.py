import cv2
import sys
sys.path.append('../')
from utils.bbox_utils import measure_distance, get_foot_position

class SpeedAndDistance_Estimator:
    
    def __init__(self):
        self.frame_window = 5
        self.frame_rate = 24

    def add_speed_and_distance_to_tracks(self, tracks: dict) -> None:
        total_distance = {}

        for category, object_tracks in tracks.items():
            if category in ["ball", "referees"]:
                continue
            number_of_frames = len(object_tracks)
            for start_frame in range(0, number_of_frames, self.frame_window):
                end_frame = min(start_frame + self.frame_window, number_of_frames - 1)
                for track_id, _ in object_tracks[start_frame].items():
                    if track_id not in object_tracks[end_frame]:
                        continue
                    start_pos = object_tracks[start_frame][track_id].get('position_transformed')
                    end_pos = object_tracks[end_frame][track_id].get('position_transformed')
                    if start_pos is None or end_pos is None:
                        continue
                    dist_covered = measure_distance(start_pos, end_pos)
                    time_elapsed = (end_frame - start_frame) / self.frame_rate
                    speed_m_s = dist_covered / time_elapsed if time_elapsed > 0 else 0
                    speed_kmh = speed_m_s * 3.6

                    if category not in total_distance:
                        total_distance[category] = {}
                    if track_id not in total_distance[category]:
                        total_distance[category][track_id] = 0
                    total_distance[category][track_id] += dist_covered

                    for frame_idx in range(start_frame, end_frame):
                        if track_id in object_tracks[frame_idx]:
                            object_tracks[frame_idx][track_id]['speed'] = speed_kmh
                            object_tracks[frame_idx][track_id]['distance'] = total_distance[category][track_id]

    def draw_speed_and_distance(self, frames: list, tracks: dict) -> list:
        output_frames = []
        for frame_num, frame in enumerate(frames):
            frame_copy = frame.copy()
            for category, object_tracks in tracks.items():
                if category in ["ball", "referees"]:
                    continue
                for _, info in object_tracks[frame_num].items():
                    speed = info.get('speed')
                    dist = info.get('distance')
                    if speed is None or dist is None:
                        continue
                    bbox = info['bbox']
                    from utils.bbox_utils import get_foot_position
                    pos = get_foot_position(bbox)
                    pos = (pos[0], pos[1] + 40)
                    cv2.putText(frame_copy, f"{speed:.2f} km/h", pos,
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
                    cv2.putText(frame_copy, f"{dist:.2f} m", (pos[0], pos[1] + 20),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
            output_frames.append(frame_copy)
        return output_frames
