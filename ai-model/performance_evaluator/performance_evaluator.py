import numpy as np
from typing import Dict, List, Any
from collections import defaultdict, Counter

class PerformanceEvaluator:
    
    def __init__(self):
        # Thresholds for goal detection (if needed)
        self.goal_x_threshold = 50
        self.goal_y_threshold = 10

    def compute_player_stats(self, tracks: Dict[str, List[Dict[Any, Any]]]) -> Dict[int, Dict[str, float]]:

        player_stats = {}
        speed_sums = defaultdict(float)
        speed_counts = defaultdict(int)

        for frame_data in tracks["players"]:
            for player_id, info in frame_data.items():
                if player_id not in player_stats:
                    player_stats[player_id] = {
                        "distance": 0.0,
                        "avg_speed": 0.0,
                        "passes": 0,
                        "goals": 0,
                        "assists": 0,
                        "possession_frames": 0,
                        "total_frames": 0,
                    }
                player_stats[player_id]["total_frames"] += 1
                if info.get("has_ball", False):
                    player_stats[player_id]["possession_frames"] += 1
                if "distance" in info:
                    current_dist = info["distance"]
                    if current_dist > player_stats[player_id]["distance"]:
                        player_stats[player_id]["distance"] = current_dist
                if "speed" in info:
                    speed_sums[player_id] += info["speed"]
                    speed_counts[player_id] += 1

        
        pass_counts = self.detect_passes(tracks)
        for pid, p_count in pass_counts.items():
            if pid in player_stats:
                player_stats[pid]["passes"] = p_count

        
        ga_counts = self.detect_goals_and_assists(tracks)
        for pid, ga_dict in ga_counts.items():
            if pid not in player_stats:
                player_stats[pid] = {
                    "distance": 0.0,
                    "avg_speed": 0.0,
                    "passes": 0,
                    "goals": 0,
                    "assists": 0,
                    "possession_frames": 0,
                    "total_frames": 0,
                }
            if "goals" in ga_dict:
                player_stats[pid]["goals"] += ga_dict["goals"]
            if "assists" in ga_dict:
                player_stats[pid]["assists"] += ga_dict["assists"]

        
        for pid in speed_sums:
            if speed_counts[pid] > 0:
                player_stats[pid]["avg_speed"] = speed_sums[pid] / speed_counts[pid]

        return player_stats

    def detect_passes(self, tracks: Dict[str, List[Dict[Any, Any]]]) -> Dict[int, int]:
        
        pass_counts = {}
        last_possessor = -1
        for frame_idx, player_dict in enumerate(tracks["players"]):
            current_possessor = -1
            for pid, info in player_dict.items():
                if info.get("has_ball", False):
                    current_possessor = pid
                    break
            if current_possessor != -1 and last_possessor != -1 and current_possessor != last_possessor:
                pass_counts[last_possessor] = pass_counts.get(last_possessor, 0) + 1
            if current_possessor != -1:
                last_possessor = current_possessor
        return pass_counts

    def detect_goals_and_assists(self, tracks: Dict[str, List[Dict[Any, Any]]]) -> Dict[int, Dict[str, int]]:
        
        ga_counts = {}
        last_possessor = -1
        second_last_possessor = -1
        frames_since_pass = 9999

        for frame_idx, player_dict in enumerate(tracks["players"]):
            current_possessor = -1
            for pid, info in player_dict.items():
                if info.get("has_ball", False):
                    current_possessor = pid
                    break
            if current_possessor != -1 and last_possessor != -1 and current_possessor != last_possessor:
                second_last_possessor = last_possessor
                last_possessor = current_possessor
                frames_since_pass = 0
            elif current_possessor != -1 and last_possessor == -1:
                last_possessor = current_possessor
                second_last_possessor = -1
                frames_since_pass = 0
            else:
                frames_since_pass += 1

            if 1 in tracks["ball"][frame_idx]:
                ball_bbox = tracks["ball"][frame_idx][1]["bbox"]
                x_center = (ball_bbox[0] + ball_bbox[2]) / 2.0
                if last_possessor != -1 and x_center < self.goal_x_threshold:
                    if last_possessor not in ga_counts:
                        ga_counts[last_possessor] = {"goals": 0, "assists": 0}
                    ga_counts[last_possessor]["goals"] += 1
                    if second_last_possessor != -1 and frames_since_pass < 30:
                        if second_last_possessor not in ga_counts:
                            ga_counts[second_last_possessor] = {"goals": 0, "assists": 0}
                        ga_counts[second_last_possessor]["assists"] += 1
                    last_possessor = -1
                    second_last_possessor = -1
                    frames_since_pass = 9999
        return ga_counts

    def evaluate_players_fifa_style(self, tracks: Dict[str, List[Dict[Any, Any]]]) -> Dict[int, Dict[str, float]]:
        
        player_stats = self.compute_player_stats(tracks)
        for pid, stats in player_stats.items():
            if stats["total_frames"] > 0:
                stats["ball_control"] = stats["possession_frames"] / stats["total_frames"]
            else:
                stats["ball_control"] = 0.0

        
        max_distance = max((p["distance"] for p in player_stats.values()), default=1)
        max_speed    = max((p["avg_speed"] for p in player_stats.values()), default=1)
        max_passes   = max((p["passes"] for p in player_stats.values()), default=1)
        max_goals    = max((p["goals"] for p in player_stats.values()), default=1)
        max_assists  = max((p["assists"] for p in player_stats.values()), default=1)

        fifa_ratings = {}
        for pid, stats in player_stats.items():
            
            pace = (stats["avg_speed"] / max_speed) * 99 if max_speed else 0

            denominator_shooting = max_goals + 0.5 * max_assists
            shooting = ((stats["goals"] + 0.5 * stats["assists"]) / denominator_shooting) * 99 if denominator_shooting else 0

            denominator_passing = max_passes + 0.5 * max_assists
            passing = ((stats["passes"] + 0.5 * stats["assists"]) / denominator_passing) * 99 if denominator_passing else 0

            dribbling = ((0.4 * (stats["avg_speed"] / max_speed) + 
                          0.3 * (stats["distance"] / max_distance) + 
                          0.3 * stats["ball_control"]) * 99) if (max_speed and max_distance) else 0

            defending = (((1 - stats["ball_control"]) * 0.5) + ((stats["distance"] / max_distance) * 0.5)) * 99 if max_distance else 0

            physical = (stats["distance"] / max_distance) * 99 if max_distance else 0

            overall = (0.3 * pace + 0.25 * dribbling + 0.2 * shooting +
                       0.1 * passing + 0.1 * physical + 0.05 * defending)

            fifa_ratings[pid] = {
                "pace": round(pace),
                "shooting": round(shooting),
                "passing": round(passing),
                "dribbling": round(dribbling),
                "defending": round(defending),
                "physical": round(physical),
                "overall": round(overall)
            }

        return fifa_ratings

def estimate_player_value_advanced(rating_dict: Dict[str, float]) -> float:
   
    pace_weight     = 1.0
    shooting_weight = 1.1
    passing_weight  = 1.2
    dribbling_weight= 1.5
    defending_weight= 0.8
    physical_weight = 1.0

    exponent     = 1.1
    scale_factor = 100
    base_value   = 5000

    pace_val   = pace_weight      * (rating_dict["pace"] ** exponent)
    shoot_val  = shooting_weight  * (rating_dict["shooting"] ** exponent)
    pass_val   = passing_weight   * (rating_dict["passing"] ** exponent)
    drib_val   = dribbling_weight * (rating_dict["dribbling"] ** exponent)
    def_val    = defending_weight * (rating_dict["defending"] ** exponent)
    phy_val    = physical_weight  * (rating_dict["physical"] ** exponent)

    attribute_sum = pace_val + shoot_val + pass_val + drib_val + def_val + phy_val
    value_in_sar = base_value + (attribute_sum * scale_factor)
    return round(value_in_sar)

