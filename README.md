# Drowsiness Detection System (DDS)

## Overview

Drowsiness Detection System (DDS) is a computer vision project designed to improve road safety by monitoring a driver's attention level in real time. The system uses a webcam and artificial intelligence techniques to detect signs of driver drowsiness and distraction. When unsafe behavior is detected, an audible alarm is triggered to alert the driver.

The project is implemented in Python using OpenCV and MediaPipe Face Mesh technology for facial landmark detection and analysis.

---

## Features

### Real-Time Face Detection

* Detects the driver's face using MediaPipe Face Mesh.
* Tracks facial landmarks continuously from the webcam feed.

### Eye Monitoring

* Extracts eye landmarks from the detected face.
* Calculates the Eye Aspect Ratio (EAR).
* Determines whether the driver's eyes are open or closed.

### Drowsiness Detection

* Monitors eye closure duration.
* Detects prolonged eye closure associated with fatigue or sleepiness.
* Activates an alarm when the driver appears drowsy.

### Distraction Detection

* Tracks head position using facial landmarks.
* Estimates whether the driver is looking away from the road.
* Activates an alarm when attention is lost for a specified duration.

### Audio Alert System

* Generates a warning sound using the computer speaker.
* Stops automatically when the driver regains attention.

### Performance Monitoring

* Displays Frames Per Second (FPS) in real time.
* Provides visual status indicators.

---

## Technologies Used

| Technology          | Purpose                            |
| ------------------- | ---------------------------------- |
| Python              | Main programming language          |
| OpenCV              | Camera access and image processing |
| MediaPipe Face Mesh | Facial landmark detection          |
| NumPy               | Numerical computations             |
| Winsound            | Audio alarm generation             |
| Threading           | Non-blocking alarm execution       |

---

## System Architecture

1. Camera captures live video.
2. Frame is processed by MediaPipe Face Mesh.
3. Facial landmarks are extracted.
4. Eye landmarks are analyzed to calculate EAR.
5. Head orientation is analyzed for distraction detection.
6. Decision module determines driver state:

   * Attentive
   * Drowsy
   * Distracted
7. Alarm system is activated if required.
8. Results are displayed on screen.

---

## Eye Aspect Ratio (EAR)

The EAR metric is used to determine whether the eyes are open or closed.

Formula:

EAR = (A + B) / (2 × C)

Where:

* A = Vertical eye distance 1
* B = Vertical eye distance 2
* C = Horizontal eye distance

A low EAR value indicates that the eyes are closed.

---

## Project Workflow

### Step 1: Capture Video

The webcam continuously captures frames.

### Step 2: Face Detection

MediaPipe Face Mesh identifies facial landmarks.

### Step 3: Landmark Extraction

Eye and nose landmarks are extracted.

### Step 4: Drowsiness Analysis

EAR is calculated and compared with a predefined threshold.

### Step 5: Distraction Analysis

Head position is analyzed relative to the camera center.

### Step 6: Warning Generation

If dangerous behavior persists:

* Visual alert is displayed.
* Audible alarm is triggered.

---

## Installation

### Clone Repository

```bash
git clone https://github.com/your-username/driver-monitoring-system.git

cd driver-monitoring-system
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Windows:

```bash
venv\Scripts\activate
```

Linux / macOS:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install opencv-python
pip install mediapipe
pip install numpy
```

Or:

```bash
pip install -r requirements.txt
```

---

## Running the Project

```bash
python main.py
```

Press:

```text
q
```

to exit the application.

---

## Project Structure

```text
Driver-Monitoring-System/
│
├── main.py
├── README.md
├── requirements.txt
│
├── assets/
│   ├── screenshots/
│   └── diagrams/
│
└── docs/
```

---

## Applications

* Smart Vehicles
* Driver Assistance Systems
* Transportation Safety
* Fleet Monitoring
* Commercial Vehicle Management
* Research in Computer Vision

---

## Future Improvements

### Head Pose Estimation

Use solvePnP for accurate head orientation tracking.

### Machine Learning Classification

Train a model to classify:

* Alert
* Drowsy
* Distracted

### Yawning Detection

Detect mouth opening as an additional fatigue indicator.

### Arduino Integration

Connect the system with:

* Buzzer
* LCD Display
* Vibration Motor

### Event Logging

Store:

* Drowsiness events
* Distraction events
* Alert history

in a database.

### Cloud Dashboard

Monitor multiple drivers remotely through a web application.

---

## Results

The system successfully:

* Detects facial landmarks in real time.
* Tracks eye movements.
* Detects prolonged eye closure.
* Identifies driver distraction.
* Generates immediate alerts.
* Maintains real-time performance suitable for prototype development.

---

## Limitations

* Performance may decrease under poor lighting conditions.
* Extreme head rotations may affect accuracy.
* Webcam quality influences detection reliability.
* Thresholds may require calibration for different users.

---

## Conclusion

This Driver Monitoring System demonstrates how computer vision and artificial intelligence can be used to improve road safety. By combining facial landmark detection, eye analysis, and attention monitoring, the system provides a practical solution for detecting drowsiness and distraction in real time.

The project serves as a strong foundation for advanced driver assistance systems (ADAS) and future intelligent transportation solutions.
