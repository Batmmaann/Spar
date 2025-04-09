SPAR
SPAR is an AI-powered system designed to analyze football matches using a single high-definition camera. By leveraging state-of-the-art computer vision and machine learning techniques, SPAR detects, tracks, and evaluates players’ performance, providing detailed insights into their skills, physical metrics, and potential market value. This tool is aimed at helping scouts, coaches, and sports analysts make informed decisions regarding talent discovery and team composition.

Table of Contents
Features

Project Structure

Installation and Setup

Usage

Modules and Data Flow

License

Features
Single-Camera Analysis: Requires only one camera covering the entire pitch.

Detection & Tracking: Uses YOLO for object detection and Deep SORT for multi-object tracking to monitor players, referees, and the ball.

Camera Movement Compensation: Estimates camera motion to stabilize tracking, even when the camera pans or zooms.

Player Metrics: Calculates key performance metrics such as speed, distance covered, and ball possession.

Team Assignment: Automatically assigns players to teams based on color analysis and other heuristics.

Performance Evaluation: Aggregates and rates player performance for talent identification and strategic decisions.

(Optional) View Transformation: Converts screen coordinates to real-world coordinates if calibration data is available.

Project Structure
pgsql
Copy
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
Key Directories:

ai-model/: Contains all modules for detection, tracking, processing, and evaluation.

dashboard/: (Optional) A web-based dashboard for visualization.

models/: Directory for storing the trained YOLO weights (models larger than 100MB should be managed via Git LFS or kept out of the repository).

Installation and Setup
Clone this repository:

bash
Copy
git clone https://github.com/Batmmaann/Spar.git
cd Spar
Create and activate a Python virtual environment (recommended):

On Linux/Mac:

bash
Copy
python3 -m venv venv
source venv/bin/activate
On Windows:

bash
Copy
python -m venv venv
venv\Scripts\activate
Install the Python dependencies:

bash
Copy
pip install -r requirements.txt
Model Weights:

Ensure your YOLO model weights (e.g., best.pt) are placed inside ai-model/models/.

For files larger than 100MB, consider using Git Large File Storage (LFS) or exclude these files from your repository.

Dashboard Setup (Optional):

If you wish to run the dashboard, navigate to the dashboard/ directory:

bash
Copy
cd dashboard
npm install
Then start the development server with:

bash
Copy
npm run dev
Open your browser at http://localhost:3000.

Usage
To run the AI pipeline, execute the following command from the project root (or from the ai-model/ directory):

bash
Copy
python server.py
What Happens:

Frame Processing: The system reads video frames from a sample video (e.g., input_videos/sample.mp4).

Detection & Tracking: YOLO detects objects and Deep SORT tracks players, referees, and the ball.

Camera Movement Estimation: The system compensates for camera panning/zoom to stabilize player positions.

Metrics & Assignment: It calculates speed, distance, ball possession, and assigns team information.

Performance Evaluation: Generates performance ratings for each player.

Output: A final annotated video is saved in output_videos/output_video.avi, which can be used for review and analysis.

Modules and Data Flow
YOLO Detection: Identifies players, referees, and the ball.

Deep SORT Tracking: Associates detections across frames to assign consistent IDs.

Camera Movement Estimator: Computes offsets to adjust coordinates.

View Transformer (Optional): Maps the in-frame positions to actual field coordinates.

Speed and Distance Estimator: Computes players' movement metrics.

Team Assigner: Determines team association and assigns colors.

Player Ball Assigner: Identifies ball possession.

Performance Evaluator: Aggregates performance metrics to rate each player.

Data Flow:

Input Video → YOLO → Detections → Deep SORT → Tracks

Camera Movement Estimation → Adjusted Tracks

Speed/Distance & Team Assignment → Performance Evaluation

Output (Annotated Video & Logs)

License
This project is open-sourced under the MIT License.
Update the license section if you have a different or more specific licensing model.

Enjoy exploring the SPAR project and leveraging AI to transform football analysis!
For any questions or contributions, please open an issue or submit a pull request.
