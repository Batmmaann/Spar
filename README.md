# SPAR: Single-Camera Player Analysis and Rating

SPAR is an AI-powered system designed to analyze football matches using a single high-definition camera. By leveraging state-of-the-art computer vision and machine learning techniques, SPAR detects, tracks, and evaluates players’ performance, providing detailed insights into their skills, physical metrics, and potential market value. This tool helps scouts, coaches, and sports analysts make informed decisions regarding talent discovery and team composition.

## Table of Contents
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation and Setup](#installation-and-setup)
- [Usage](#usage)
- [Modules and Data Flow](#modules-and-data-flow)
- [License](#license)

## Features
- **Single-Camera Analysis**: Requires only one camera covering the entire pitch.
- **Detection & Tracking**: Uses YOLO for object detection and Deep SORT for multi-object tracking to monitor players, referees, and the ball.
- **Camera Movement Compensation**: Estimates camera motion to stabilize tracking, even when the camera pans or zooms.
- **Player Metrics**: Calculates key performance metrics such as speed, distance covered, and ball possession.
- **Team Assignment**: Automatically assigns players to teams based on color analysis and other heuristics.
- **Performance Evaluation**: Aggregates and rates player performance for talent identification and strategic decisions.
- **(Optional) View Transformation**: Converts screen coordinates to real-world coordinates if calibration data is available.

## Project Structure
SPAR
├── ai-model
│ ├── camera_movement_estimator
│ ├── deep_sort_tracker
│ ├── player_ball_assigner
│ ├── performance_evaluator
│ ├── speed_and_distance_estimator
│ ├── team_assigner
│ ├── utils
│ ├── view_transformer
│ ├── server.py <-- Primary entry point for the AI pipeline
│ └── models <-- Contains YOLO model weights (use Git LFS or exclude)
├── dashboard <-- (Optional) Front-end to visualize results
│ ├── public
│ ├── src
│ ├── package.json
│ └── next.config.js
├── requirements.txt <-- Python dependencies
├── .gitignore
└── README.md <-- This file

Copy

**Key Directories**:
- `ai-model/`: Modules for detection, tracking, processing, and evaluation.
- `dashboard/`: (Optional) Web-based dashboard for visualization.
- `models/`: Directory for YOLO weights (manage large files via Git LFS).

## Installation and Setup
1. **Clone the repository**:
   ```bash
   git clone https://github.com/Batmmaann/Spar.git
   cd Spar
Create and activate a Python virtual environment:

Linux/Mac:

bash
Copy
python3 -m venv venv
source venv/bin/activate
Windows:

bash
Copy
python -m venv venv
venv\Scripts\activate
Install dependencies:

bash
Copy
pip install -r requirements.txt
Model Weights:

Place YOLO weights (e.g., best.pt) in ai-model/models/.

Use Git LFS for files >100MB or exclude them.

(Optional) Dashboard Setup:

bash
Copy
cd dashboard
npm install
npm run dev  # Starts dev server at http://localhost:3000
Usage
Run the AI pipeline from the project root:

bash
Copy
python server.py
Process Overview:

Frame Processing: Reads video from input_videos/sample.mp4.

Detection & Tracking: YOLO and Deep SORT track objects.

Camera Stabilization: Adjusts for camera movement.

Metrics & Assignment: Computes speed, distance, team, and ball possession.

Evaluation: Generates player ratings.

Output: Annotated video saved to output_videos/output_video.avi.

Modules and Data Flow
YOLO Detection: Identifies players, referees, and the ball.

Deep SORT Tracking: Assigns consistent IDs across frames.

Camera Movement Estimator: Stabilizes coordinates during camera motion.

View Transformer: Maps frame positions to real-world coordinates (optional).

Speed/Distance Estimator: Calculates movement metrics.

Team Assigner: Determines team associations.

Player Ball Assigner: Tracks ball possession.

Performance Evaluator: Aggregates metrics into ratings.

Data Flow:

Copy
Input Video → YOLO → Detections → Deep SORT → Tracks
            ↓
Camera Movement Estimation → Adjusted Tracks → Speed/Distance & Team Assignment → Performance Evaluation → Output
License
This project is licensed under the MIT License. See LICENSE for details.

Explore SPAR and transform football analysis with AI! For questions or contributions, open an issue or submit a pull request.
