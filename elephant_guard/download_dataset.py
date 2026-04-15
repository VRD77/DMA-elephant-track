import os
import subprocess
import sys

def main():
    print("Welcome to ElephantGuard Dataset Downloader!")
    print("This script uses the OpenImages V7 dataset to fetch raw Elephant images.")
    
    # Check if openimages is installed
    try:
        import openimages
    except ImportError:
        print("openimages package not found. Installing via pip...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "openimages"])
    
    base_dir = "./elephant_dataset_raw"
    images_dir = os.path.join(base_dir, "elephant", "images")
    
    os.makedirs(base_dir, exist_ok=True)
    
    print(f"\nDownloading Elephant dataset from Open Images into {base_dir} ...")
    print("This may take a while depending on your internet connection.")
    
    cmd = "oi_download_dataset --base_dir ./elephant_dataset_raw --labels Elephant --format darknet --limit 500"
    
    try:
        subprocess.run(cmd, check=True, shell=True)
        print("\nDownload complete!")
        print(f"Your raw images are located inside: {images_dir}")
        print("\nNEXT STEPS:")
        print("1. Upload these images to Roboflow.")
        print("2. Add 20-30 pictures of elephants on *phone screens* in front of your webcam.")
        print("3. Annotate and configure augmentations (Flip, Brightness, Blur, Mosaic).")
        print("4. Export from Roboflow as YOLOv8 PyTorch format into ./elephant_dataset/")
    except subprocess.CalledProcessError as e:
        print(f"\nError occurred during download: {e}")
        print("Try manually running: oi_download_dataset --base_dir ./elephant_dataset_raw --labels Elephant --format darknet")

if __name__ == "__main__":
    main()
