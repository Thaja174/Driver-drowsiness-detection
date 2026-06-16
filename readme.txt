Driver fatigue is one of the leading causes of road accidents worldwide. This project presents a real-time Driver Drowsiness Monitoring and Vehicle Safety Control System developed using Computer Vision, MediaPipe, and the Quanser QLabs QCar2 simulation platform.

The system continuously monitors the driver's facial features through a webcam, detects signs of drowsiness using Eye Aspect Ratio (EAR) and Head Pose Analysis, and automatically intervenes when unsafe driving conditions are detected.

To reduce false alarms, an interactive driver validation mechanism is implemented. Instead of immediately classifying the driver as drowsy, the system asks the driver to respond to a challenge using a randomly selected arrow key. If the driver fails to respond within the specified time, the vehicle remains stopped to ensure safety.

Webcam Input
      │
      ▼
Face Detection & Landmark Extraction
      │
      ▼
EAR Calculation + Head Pose Analysis
      │
      ▼
Drowsiness Detection Engine
      │
      ▼
Interactive Validation System
      │
      ├── Driver Responds
      │         │
      │         ▼
      │    Resume Monitoring
      │
      └── No Response
                │
                ▼
         Vehicle Stopped
