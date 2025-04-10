# SPAR: Single-Camera Player Analysis and Rating

SPAR is an AI-powered system designed to analyze football matches using a single high-definition camera. Leveraging state-of-the-art computer vision and machine learning techniques, SPAR detects, tracks, and evaluates players' performance, providing detailed insights into their skills, physical metrics, and potential market value. This tool aids scouts, coaches, and sports analysts in making informed decisions regarding talent discovery and team composition.

## Table of Contents
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation and Setup](#installation-and-setup)
- [Usage](#usage)
- [Modules and Data Flow](#modules-and-data-flow)
- [License](#license)

## Features

- **Single-Camera Analysis:** Utilizes one camera covering the entire pitch.
- **Detection & Tracking:** Integrates YOLO for object detection and Deep SORT for multi-object tracking to monitor players, referees, and the ball.
- **Camera Movement Compensation:** Estimates and compensates for camera motion (panning/zooming) to provide stable tracking.
- **Player Metrics:** Computes key performance indicators such as speed, distance covered, and ball possession.
- **Team Assignment:** Automatically assigns players to teams using color analysis and additional heuristics.
- **Performance Evaluation:** Aggregates and rates player performance to assist with talent identification and strategic decisions.
- **(Optional) View Transformation:** Converts screen coordinates to real-world field coordinates when calibration data is available.

## Project Structure

```
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
│   └── models                   <-- Contains YOLO model weights (manage with Git LFS if >100MB)
├── dashboard                    <-- (Optional) Front-end to visualize results
│   ├── public
│   ├── src
│   ├── package.json
│   └── next.config.js
├── requirements.txt             <-- Python dependencies
├── .gitignore
└── README.md                    <-- This file
```

## Installation and Setup

### Clone the Repository

Clone this repository using Git:

```bash
git clone https://github.com/Batmmaann/Spar.git
cd Spar
```

### Create and Activate a Virtual Environment

It is recommended to use a Python virtual environment.

#### On Linux/Mac:
```bash
python3 -m venv venv
source venv/bin/activate
```

#### On Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

### Install Python Dependencies

Install the required libraries:
```bash
pip install -r requirements.txt
```

### Model Weights

Ensure your YOLO model weights (e.g., `best.pt`) are placed inside the `ai-model/models/` directory.
For files larger than 100MB, consider using Git LFS or exclude these files from your repository.

### (Optional) Dashboard Setup

If you wish to run the dashboard for visualization, follow these steps:

Navigate to the dashboard directory:
```bash
cd dashboard
```

Install Node.js dependencies:
```bash
npm install
```

Start the development server:
```bash
npm run dev
```

Open your browser and go to [http://localhost:3000](http://localhost:3000).

## Usage

To run the AI pipeline, execute the following command from the project root (or from the `ai-model/` directory):

```bash
python server.py
```

### What Happens Under the Hood

1. **Frame Processing:** Reads video frames from a source file (e.g., `input_videos/sample.mp4`).
2. **Detection & Tracking:** YOLO identifies objects and Deep SORT associates detections across frames.
3. **Camera Movement Estimation:** Compensates for any camera panning/zoom to stabilize the tracking.
4. **Metrics & Assignment:** Calculates speed, distance, ball possession, and assigns team colors.
5. **Performance Evaluation:** Generates performance ratings for each player.
6. **Output:** Produces an annotated video saved to `output_videos/output_video.avi` for review and further analysis.

## Modules and Data Flow

1. **YOLO Detection:** Identifies players, referees, and the ball.
2. **Deep SORT Tracking:** Links detections across frames to assign consistent IDs.
3. **Camera Movement Estimator:** Calculates offsets to adjust for camera movement.
4. **(Optional) View Transformer:** Maps in-frame positions to actual field coordinates.
5. **Speed and Distance Estimator:** Computes movement metrics for each player.
6. **Team Assigner:** Determines team affiliation based on uniform colors.
7. **Player Ball Assigner:** Detects ball possession.
8. **Performance Evaluator:** Aggregates and rates the performance metrics.

### Data Flow Overview

```plaintext
Input Video → YOLO Detection → Detections → Deep SORT Tracking → Tracks
             ↓
      Camera Movement Estimation → Adjusted Tracks
             ↓
  Speed/Distance & Team Assignment → Performance Evaluation
             ↓
 Output (Annotated Video & Logs)
```

## License

This project is open-sourced under the MIT License.
If you have a different licensing model, please update this section accordingly.
