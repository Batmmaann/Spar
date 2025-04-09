import numpy as np
import cv2

class ViewTransformer:
    
    def __init__(self) -> None:
        
        court_width = 68.0
        court_length = 105.0

        self.pixel_vertices = np.array([
            [110, 1035],
            [265, 275],
            [910, 260],
            [1640, 915]
        ], dtype=np.float32)

        self.target_vertices = np.array([
            [0, court_width],       
            [0, 0],                 
            [court_length, 0],      
            [court_length, court_width]  
        ], dtype=np.float32)

        self.perspective_transform = cv2.getPerspectiveTransform(self.pixel_vertices, self.target_vertices)

    def transform_point(self, point: np.ndarray) -> np.ndarray:
        if point.shape == (2,):
            point = point.reshape(1, 1, 2).astype(np.float32)
        elif point.shape == (1, 2):
            point = point.reshape(1, 1, 2).astype(np.float32)

        transformed = cv2.perspectiveTransform(point, self.perspective_transform)
        return transformed.reshape(-1)

    def add_transformed_position_to_tracks(self, tracks: dict) -> None:
        for category, frames in tracks.items():
            for frame_num, track_dict in enumerate(frames):
                for track_id, info in track_dict.items():
                    if 'position_adjusted' not in info:
                        continue
                    pos_adj = np.array(info['position_adjusted'], dtype=np.float32)
                    pos_adj = pos_adj.reshape(1, 1, 2)
                    transformed = cv2.perspectiveTransform(pos_adj, self.perspective_transform)
                    info['position_transformed'] = transformed[0, 0].tolist()
