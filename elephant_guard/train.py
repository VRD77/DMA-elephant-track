from ultralytics import YOLO

def main():
    print("Initiating Custom YOLOv8 Elephant Warning Model Training Pipeline...")
    
    # nano - fastest for CPU demo
    model = YOLO("yolov8n.pt")   
    
    results = model.train(
        data="elephant_dataset/data.yaml",
        epochs=50,               # 50 enough for small dataset
        imgsz=640,
        batch=8,                 # reduce to 4 if RAM < 8GB
        patience=10,             # early stop if no improvement
        lr0=0.01,
        lrf=0.001,
        mosaic=1.0,
        flipud=0.0,
        fliplr=0.5,
        degrees=10.0,
        translate=0.1,
        scale=0.5,
        hsv_h=0.015,
        hsv_s=0.7,
        hsv_v=0.4,
        device="cpu",            # No GPU selected per user constraints
        workers=2,
        project="runs/train",
        name="elephant_v1",
        exist_ok=True,
        pretrained=True,         # transfer learning from COCO weights
        verbose=True
    )

    print("Best model saved at:", results.save_dir)

    # After training, evaluate on test set:
    metrics = model.val(data="elephant_dataset/data.yaml", split="test")
    print(f"mAP50: {metrics.box.map50:.3f}")
    print(f"Precision: {metrics.box.p:.3f}")
    print(f"Recall: {metrics.box.r:.3f}")

    # Export to ONNX for faster CPU inference:
    print("Exporting to ONNX layout...")
    model.export(format="onnx", imgsz=640, simplify=True)
    # Exported model: runs/train/elephant_v1/weights/best.onnx
    print("Model ready!")

if __name__ == "__main__":
    main()
