import sys
sys.path.append('../')
from utils.bbox_utils import get_center_of_bbox, measure_distance

class PlayerBallAssigner:
    def __init__(self) -> None:
        self.max_player_ball_distance = 70

    def assign_ball_to_player(self, players: dict, ball_bbox: list) -> int:
        ball_position = get_center_of_bbox(ball_bbox)
        min_dist = float('inf')
        assigned_player = -1
        for player_id, info in players.items():
            bbox = info['bbox']
            dist_left = measure_distance((bbox[0], bbox[3]), ball_position)
            dist_right = measure_distance((bbox[2], bbox[3]), ball_position)
            dist = min(dist_left, dist_right)
            if dist < self.max_player_ball_distance and dist < min_dist:
                min_dist = dist
                assigned_player = player_id
        return assigned_player
