from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from performance_evaluator import PerformanceEvaluator, estimate_player_value_advanced
from deep_sort_tracker import DeepSortTracker
from camera_movement_estimator import CameraMovementEstimator
from view_transformer import ViewTransformer
from speed_and_distance_estimator import SpeedAndDistance_Estimator
from team_assigner import TeamAssigner
from player_ball_assigner import PlayerBallAssigner
from Re_ID.track_postprocess import filter_short_lived_ids, reid_merge_tracks, keep_top_22_ids
from Re_ID.reid_model import ReIDModel
from utils.video_utils import read_video

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_methods=["*"],
    allow_headers=["*"],
)

fifa_ratings: dict = {}

def process_video(video_path: str) -> dict:
    frames = read_video(video_path)
    tracker = DeepSortTracker(model_path='models/best.pt', device='cuda')
    tracks = tracker.get_object_tracks(frames)
    tracker.add_position_to_tracks(tracks)

    cam = CameraMovementEstimator(frames[0])
    offsets = cam.get_camera_movement(frames)
    cam.add_adjust_positions_to_tracks(tracks, offsets)

    transformer = ViewTransformer()
    transformer.add_transformed_position_to_tracks(tracks)

    tracks["ball"] = tracker.interpolate_ball_positions(tracks["ball"])
    SpeedAndDistance_Estimator().add_speed_and_distance_to_tracks(tracks)

    team = TeamAssigner()
    first_frame = next((i for i, p in enumerate(tracks["players"]) if p), -1)
    if first_frame != -1:
        team.assign_team_color(frames[first_frame], tracks["players"][first_frame])
    for i, players in enumerate(tracks["players"]):
        for pid, info in players.items():
            info['team'] = team.get_player_team(frames[i], info['bbox'], pid)

    ball_assigner = PlayerBallAssigner()
    for i, players in enumerate(tracks["players"]):
        if 1 in tracks["ball"][i]:
            pid = ball_assigner.assign_ball_to_player(players, tracks["ball"][i][1]['bbox'])
            if pid != -1:
                players[pid]['has_ball'] = True

    filter_short_lived_ids(tracks)
    reid_merge_tracks(tracks, frames, ReIDModel(), threshold=0.7)
    keep_top_22_ids(tracks)

    return PerformanceEvaluator().evaluate_players_fifa_style(tracks)

@app.post("/upload")
async def upload_video(file: UploadFile = File(...)):
    video_path = "uploaded_video.mp4"
    with open(video_path, "wb") as f:
        f.write(await file.read())

    global fifa_ratings
    fifa_ratings = process_video(video_path)

    sorted_stats = sorted(fifa_ratings.items(), key=lambda x: x[1]['overall'], reverse=True)
    output = []
    for new_id, (orig_track_id, stats) in enumerate(sorted_stats, start=1):
        output.append({
            "id": new_id,
            "track_id": orig_track_id,
            **stats,
            "value": estimate_player_value_advanced(stats)
        })

    return {"message": "Video processed successfully", "players": output}

@app.get("/api/players")
def get_players():
    sorted_stats = sorted(fifa_ratings.items(), key=lambda x: x[1]['overall'], reverse=True)
    return [
        {
            "id": idx,
            "track_id": orig,
            **stats,
            "value": estimate_player_value_advanced(stats)
        }
        for idx, (orig, stats) in enumerate(sorted_stats, start=1)
    ]

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
