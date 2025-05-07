from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import uvicorn
import cv2
import time
import numpy as np
import supervision as sv

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

GLOBAL = {
    "frames":       None,
    "tracks":       None,
    "yolo_results": None,
    "stats":        None,
    "team_cols":    None,
    "fps":          24.0,
}

@app.post("/upload")
async def upload_video(file: UploadFile = File(...)):
    path = "uploaded_video.mp4"
    with open(path, "wb") as f:
        f.write(await file.read())

    cap = cv2.VideoCapture(path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 24.0
    cap.release()

    frames = read_video(path)

    tracker      = DeepSortTracker(model_path="models/best.pt", device="cuda")
    yolo_results = tracker.detect_frames(frames)

    tracks  = tracker.get_object_tracks(frames)
    tracker.add_position_to_tracks(tracks)

    cam     = CameraMovementEstimator(frames[0])
    offsets = cam.get_camera_movement(frames)
    cam.add_adjust_positions_to_tracks(tracks, offsets)

    transformer = ViewTransformer()
    transformer.add_transformed_position_to_tracks(tracks)

    tracks["ball"] = tracker.interpolate_ball_positions(tracks["ball"])
    SpeedAndDistance_Estimator().add_speed_and_distance_to_tracks(tracks)

    team  = TeamAssigner()
    first = next((i for i,p in enumerate(tracks["players"]) if p), -1)
    if first >= 0:
        team.assign_team_color(frames[first], tracks["players"][first])

    assigner = PlayerBallAssigner()
    for i, players in enumerate(tracks["players"]):
        for pid, info in players.items():
            info["team"] = team.get_player_team(frames[i], info["bbox"], pid)
        if 1 in tracks["ball"][i]:
            pid = assigner.assign_ball_to_player(players, tracks["ball"][i][1]["bbox"])
            if pid != -1:
                players[pid]["has_ball"] = True

    filter_short_lived_ids(tracks)
    reid_merge_tracks(tracks, frames, ReIDModel(), threshold=0.7)
    keep_top_22_ids(tracks)

    stats = PerformanceEvaluator().evaluate_players_fifa_style(tracks)

    GLOBAL.update({
        "frames":       frames,
        "tracks":       tracks,
        "yolo_results": yolo_results,
        "stats":        stats,
        "team_cols":    team.team_colors,
        "fps":          fps,
    })

    output = []
    for idx, (orig, st) in enumerate(
        sorted(stats.items(), key=lambda x: x[1]["overall"], reverse=True),
        start=1
    ):
        output.append({
            "id":        idx,
            "track_id":  orig,
            **st,
            "value":     estimate_player_value_advanced(st),
        })

    return {"message": "Processed", "players": output}

@app.get("/api/players")
def get_players():
    stats = GLOBAL["stats"] or {}
    return [
        {
            "id":        idx,
            "track_id":  orig,
            **st,
            "value":     estimate_player_value_advanced(st),
        }
        for idx, (orig, st) in enumerate(
            sorted(stats.items(), key=lambda x: x[1]["overall"], reverse=True),
            start=1
        )
    ]

@app.get("/video_feed")
def video_feed():
    frames       = GLOBAL["frames"]
    yolo_results = GLOBAL["yolo_results"]
    team_cols    = GLOBAL["team_cols"]
    fps          = GLOBAL.get("fps", 24.0)
    interval     = 1.0 / fps

    palette = sv.ColorPalette.from_hex([
        '#{:02X}{:02X}{:02X}'.format(*team_cols[1]),
        '#{:02X}{:02X}{:02X}'.format(*team_cols[2]),
        '#FFFF00',
        '#FF0000',
    ])
    box_annotator   = sv.BoxAnnotator(color=palette, thickness=2)
    label_annotator = sv.LabelAnnotator(
        color=palette,
        text_color=sv.Color.from_hex('#FFFFFF'),
        text_scale=0.5
    )

    def gen():
        for idx, frame in enumerate(frames):
            start = time.time()

            # convert the Ultralytics Results → Supervision Detections
            result = yolo_results[idx]
            dets   = sv.Detections.from_ultralytics(result)

            # build labels from the model's names & confidences
            labels = [
                f"{result.names[cid]} {conf:.2f}"
                for cid, conf in zip(dets.class_id, dets.confidence)
            ]

            # draw tight YOLO boxes + labels
            annotated = box_annotator.annotate(scene=frame, detections=dets)
            annotated = label_annotator.annotate(
                scene      = annotated,
                detections = dets,
                labels     = np.array(labels)
            )

            annotated = cv2.resize(annotated, (640, 360))
            _, jpg = cv2.imencode('.jpg', annotated)

            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n"
                + jpg.tobytes()
                + b"\r\n"
            )

            elapsed = time.time() - start
            if elapsed < interval:
                time.sleep(interval - elapsed)

    return StreamingResponse(
        gen(),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
