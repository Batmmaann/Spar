from sklearn.cluster import KMeans
import numpy as np
import cv2
from typing import Dict, Any

class TeamAssigner:

    def __init__(self) -> None:
        self.team_colors: Dict[int, tuple] = {}
        self.player_team_dict: Dict[int, int] = {}

    def get_clustering_model(self, image: np.ndarray) -> KMeans:
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        image_2d = lab.reshape(-1, 3)
        kmeans = KMeans(n_clusters=2, init="k-means++", n_init=1)
        kmeans.fit(image_2d)
        return kmeans

    def get_player_color(self, frame: np.ndarray, bbox: list) -> np.ndarray:
        x1, y1, x2, y2 = map(int, bbox)
        image = frame[y1:y2, x1:x2]
        if image.size == 0:
            return np.array([0, 128, 128], dtype=np.float32)
        top_half_image = image[0:int(image.shape[0] / 2), :]
        kmeans = self.get_clustering_model(top_half_image)
        labels = kmeans.labels_
        clustered_image = labels.reshape(top_half_image.shape[0], top_half_image.shape[1])
        corner_clusters = [
            clustered_image[0, 0],
            clustered_image[0, -1],
            clustered_image[-1, 0],
            clustered_image[-1, -1]
        ]
        non_player_cluster = max(set(corner_clusters), key=corner_clusters.count)
        player_cluster = 1 - non_player_cluster
        return kmeans.cluster_centers_[player_cluster]

    def assign_team_color(self, frame: np.ndarray, player_detections: Dict[Any, Any]) -> None:
        if not player_detections:
            print("Warning: No player detections available for team assignment.")
            return
        lab_colors = []
        for _, detection in player_detections.items():
            bbox = detection["bbox"]
            lab_color = self.get_player_color(frame, bbox)
            lab_colors.append(lab_color)
        if not lab_colors:
            print("Warning: No LAB colors extracted from player detections.")
            return
        lab_colors = np.array(lab_colors, dtype=np.float64)
        kmeans = KMeans(n_clusters=2, init="k-means++", n_init=10)
        kmeans.fit(lab_colors)
        lab_centers = kmeans.cluster_centers_.reshape(1, -1, 3).astype(np.uint8)
        bgr_centers = cv2.cvtColor(lab_centers, cv2.COLOR_Lab2BGR)[0]
        self.team_colors[1] = tuple(map(int, bgr_centers[0]))
        self.team_colors[2] = tuple(map(int, bgr_centers[1]))
        self.kmeans = kmeans

    def get_player_team(self, frame: np.ndarray, player_bbox: list, player_id: int) -> int:
        if not hasattr(self, 'kmeans'):
            return 1
        if player_id in self.player_team_dict:
            return self.player_team_dict[player_id]
        lab_color = self.get_player_color(frame, player_bbox).reshape(1, -1).astype(np.float64)
        team_index = int(self.kmeans.predict(lab_color)[0])
        team_id = team_index + 1
        if player_id == 91:
            team_id = 1
        self.player_team_dict[player_id] = team_id
        return team_id
