# SPAR: Single-Camera Player Analysis and Rating

SPAR is an AI-powered system designed to analyze football matches using a single high-definition camera. By leveraging state-of-the-art computer vision and machine learning techniques, SPAR detects, tracks, and evaluates players’ performance, providing detailed insights into their skills, physical metrics, and potential market value. This tool is aimed at helping scouts, coaches, and sports analysts make informed decisions regarding talent discovery and team composition.

---

## Table of Contents

1. [Features](#features)  
2. [Project Structure](#project-structure)  
3. [Installation and Setup](#installation-and-setup)  
4. [Usage](#usage)  
5. [Modules and Data Flow](#modules-and-data-flow)  
6. [License](#license)

---

## Features

- **Single-Camera Analysis:** Requires only one camera covering the entire pitch.  
- **Detection & Tracking:** Uses YOLO for object detection and Deep SORT for multi-object tracking to monitor players, referees, and the ball.  
- **Camera Movement Compensation:** Estimates camera motion to stabilize tracking, even if the camera pans or zooms.  
- **Player Metrics:** Calculates key performance metrics such as speed, distance covered, and ball possession.  
- **Team Assignment:** Automatically assigns players to teams based on color detection and strategic decisions.  
- **Performance Evaluation:** Aggregates and rates player performance for talent identification and strategic decisions.  
- **(Optional) View Transformation:** Converts screen coordinates to real-world coordinates if calibration data is available.

---

## Project Structure

```text
SPAR
├── ai-model
│   ├── camera_movement_estimator
│   ├── deep_sort_tracker
│   ├── player_ball_assigner
│   ├── performance_evaluator
│   ├── speed_and_distance_estimator
│   ├── team_assigner
│   ├── utils
│   ├── view_transformer
│   ├── server.py                <-- Primary entry point for the AI pipeline
│   └── models                   <-- Contains your YOLO model weights (use Git LFS or exclude)
├── dashboard                   <-- (Optional) Front-end to visualize results
│   ├── public
│   ├── src
│   ├── package.json
│   └── next.config.js
├── requirements.txt            <-- Python dependencies
├── .gitignore
└── README.md                   <-- This file
