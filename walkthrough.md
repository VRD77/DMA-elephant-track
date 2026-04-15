# ElephantGuard System Enhancements & Bug Fixes

This document serves as a detailed breakdown of the optimizations, structural changes, and bug fixes applied to the ElephantGuard Wildlife Detection system to resolve application lag, missing alerts, and environmental crashes.

## 1. Environment & API Stabilization

> [!WARNING] 
> The initial implementation relied on the legacy `mediapipe.solutions` API, which has been removed in the MediaPipe module binaries available for **Python 3.13**. 

- **Issue:** The application suffered immediate crashes on initialization due to `AttributeError: module 'mediapipe' has no attribute 'solutions'`.
- **Solution:** 
  - Downloaded the prerequisite `hand_landmarker.task` weights bundle.
  - Refactored `finger_motion_tracker.py` to utilize the modern `mediapipe.tasks.python.vision.HandLandmarker` API.
  - Adapted the coordinate extraction mechanics to interpret the new normalized landmark lists provided by the Tasks API without breaking downstream dependencies.

## 2. Performance & Display Frame Rates

> [!CAUTION]
> Running the YOLOv8 model synchronously on every single full-resolution frame is highly computationally expensive on the CPU, causing severe UI lag (as low as 3 – 5 FPS).

- **Issue:** Users reported the application felt "laggy" and stuttered when tracking movement, destroying the responsiveness of the demo.
- **Solution:** 
  - Modified `main.py` to implement a **Frame Skipping Architecture**.
  - YOLOv8 inference now runs entirely on **1 out of every 3 frames**. 
  - For frames where inference is skipped, the rendering engine securely caches and redraws the last known human bounding boxes coordinates to maintain 100% visual stability without screen flickering.
  - **Result:** Drastically smoothed out the real-time webcam rendering loop.

## 3. Finger Tracking Motion Sensitivities

- **Issue:** The tracker frequently failed to recognize a finger unless it was pointed straight upwards vertically. If the user pointed horizontally across the screen camera feed, it failed the rigid "Index Tip Y-coordinate < PIP Y-coordinate" heuristic.
- **Solution:** 
  - Substantially relaxed the `_is_index_extended()` rules in `finger_motion_tracker.py`. As long as the MediaPipe engine recognizes the user's hand, it now continuously latches onto the presence of the index finger point structure, vastly improving tracking stability for sideways swipes.

## 4. Alert Engine Thresholding

> [!IMPORTANT]
> Because of CPU lag, frame captures were stretched out over time. The application failed to trigger the desktop notification because it was nearly impossible for a user to drag their finger across 20 distinct frames rapidly while simultaneously keeping vertical movement within extremely precise geometric thresholds.

- **Issue:** The `Elephant is crossing` warning log and desktop notification never deployed despite large swathes of horizontal user movement. 
- **Solution:**
  - Rescaled the constants inside `config.py` explicitly for a lower-FPS target.
  - **`FINGER_TRAIL_LENGTH`** reduced from 20 -> 10 frames.
  - **`SUSTAINED_FRAMES`** required to define an undeniable elephant crossing cut from 15 -> 3 uninterrupted frames.
  - **`HORIZONTAL_DELTA_MIN`** dropped from 120 pixels -> 80 pixels.
  - **`VERTICAL_DELTA_MAX`** widened from 60 pixels -> 80 pixels (more tolerance for wobbly pointing).
  - **Result:** The system is vastly more trigger-forgiving and will pop the correct warnings in the CLI and flashing visuals upon swift, noticeable gesture motions.
