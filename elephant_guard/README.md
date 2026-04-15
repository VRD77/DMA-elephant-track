# ElephantGuard — Custom YOLOv8 Wildlife Detector

ElephantGuard is a desktop-based computer vision application designed to simulate an intelligent edge-computing camera trap. It utilizes a custom-trained YOLOv8 model capable of accurately identifying an elephant traversing across a video feed, logging the trajectory, and triggering real-time cross-platform visual and audio warnings.

## Architecture Update

This repository has transitioned from using a MediaPipe proxy finger-tracker to a **genuine, custom YOLOv8 elephant tracking model**.

### Project Deliverables Matrix
- [x] `train.py` — High-efficiency custom YOLO training loop wrapper.
- [x] `download_dataset.py` — Automated fetch script for OpenImages.
- [x] `yolo_detector.py` — Custom detector bounding box and directional tracking class.
- [x] `main.py` — Execution loop and camera synchronization pipeline.
- [x] `display_renderer.py` — Real-time tracking HUD rendering pipeline.

---

## 1. Setup & Installation

Ensure you are running Python 3.9 - 3.13.

```bash
pip install -r requirements.txt
```

---

## 2. Dataset Pipeline & Model Training

Because this system runs a specialized demonstration predicting screens on a phone held to a webcam, you must compile and train the custom YOLOv8 weights before deploying the demo.

### Step 1: Download Core Images
Run the automated fetch script to download raw elephant images from the OpenImages dataset:
```bash
python download_dataset.py
```

### Step 2: Roboflow Annotation
1. Upload the downloaded images to a Free Roboflow account.
2. IMPORTANT: **Add 20-30 photographs taken of an elephant picture displayed on your phone screen held up to your webcam** (this is critical to tune the YOLO model for the demonstration environment).
3. Annotate the "elephant" class. 
4. Apply the following augmentations: Horizontal Flip, Brightness ±25%, Blur 1.5px, Rotation ±10°, Mosaic.
5. Export as **YOLOv8 PyTorch** into an `elephant_dataset/` directory at the project root.

### Step 3: Train the Classifier
Launch the highly-parameterized training script:
```bash
python train.py
```
This will autonomously parse your `elephant_dataset`, train `yolov8n.pt` over 50 epochs, export the layout as ONNX, and store your final weights at `runs/train/elephant_v1/weights/best.pt`.

---

## 3. Demonstration Walkthrough

Once you have successfully executed Phase 2 and your `best.pt` model weights exist, execute the main detector:

```bash
python main.py
```

To demonstrate the system:
1. Open a large, clear elephant image on your phone (A side-profile silhouette works best because of its distinct shape).
2. Ensure the image is full-screen on your phone with no white borders. High-contrast images are highly preferred.
3. Hold the phone approximately **40–60 cm** from your laptop webcam.
4. **Slowly move the phone LEFT to RIGHT** across the camera field (simulate an elephant crossing a highway).
5. The system will detect the elephant, draw a green bounding box bounding it, chart the centerpoint movement along a dot trajectory, and fire the `ELEPHANT CROSSING DETECTED` red-tint flash within 1-2 seconds.
6. Check `alerts_log.csv` to see the documented crossing anomaly logs.

Press `q` within the viewing window to exit gracefully at any time.
