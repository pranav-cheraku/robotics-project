# Roomba Goalie

A computer vision-powered iRobot Create 3 that acts as a goalie, detecting and blocking incoming balls using real-time object detection.

**Team:** Pranav Cheraku, Jeffrey Guo, Isaiah Hardy, Grayson Koch

---

## Overview

Our Roomba goalie uses a phone camera and computer vision to track a tennis ball and direct an iRobot Create 3 to block it from entering a goal area. The system detects the ball's position in the camera frame, determines which direction to move, and sends movement commands to the Roomba over Bluetooth.


## How It Works

The system follows a **Sense → Think → Act** pipeline:

### Sense
- A phone mounted on the Roomba streams video as the camera input
- Object detection is handled by **OpenCV** with a model trained on a public dataset via **Roboflow**
- The model identifies tennis balls in each frame and returns their position

### Think
- The camera frame is split into three zones: **left**, **center**, and **right**
- The system uses a greedy strategy: keep the detected object centered in the frame
- If the ball appears on the left, the Roomba moves left; if on the right, it moves right; if centered, it holds position

### Act
- Commands are sent to the iRobot Create 3 via the **Python SDK** over **Bluetooth Low Energy (BLE)**
- The robot translates BLE commands into ROS 2 actions internally
- Movement is constrained to a single axis (left/right along the goal line), reducing complexity and error

