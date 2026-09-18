# Vision3D — Modular Computer Vision Toolkit

Vision3D is a command-line Computer Vision toolkit for CSE3010 that combines image enhancement, feature extraction/matching, projective geometry, segmentation, camera calibration/rectification, stereo depth estimation, and 3D point-cloud reconstruction.

## Modules
1. Image preprocessing: grayscale, Gaussian/median filtering, histogram equalization, Canny edges.
2. Feature extraction and matching: Harris, SIFT, BFMatcher and Lowe ratio test.
3. Homography and RANSAC: robust projective transformation estimation and perspective warping.
4. Image segmentation: Otsu thresholding, edge-based segmentation, region growing and mean-shift.
5. Camera calibration and stereo rectification: chessboard calibration and rectification using intrinsic/extrinsic parameters.
6. Stereo depth and 3D reconstruction: SGBM disparity, depth estimation and ASCII PLY point cloud.

## Requirements
- Python 3.10+
- OpenCV
- NumPy
- pytest

## Setup
```powershell
python -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pytest -q
```

## Commands

### Preprocessing
```powershell
python main.py preprocess --input data/input/sample.jpg
```

### Features
```powershell
python main.py features --image1 data/input/sample.jpg --image2 data/input/image2.jpg
```

### Homography + RANSAC
```powershell
python main.py homography --image1 data/input/sample.jpg --image2 data/input/image2.jpg
```

### Segmentation
```powershell
python main.py segment --input data/input/sample.jpg --method all
```
Methods: `otsu`, `edge`, `region`, `mean_shift`, `all`.

### Stereo depth
The pair must have identical dimensions and should ideally be rectified.
```powershell
python main.py stereo --left data/stereo/left.png --right data/stereo/right_resized.png
```

### Camera calibration
Put chessboard calibration images in `data/calibration/`.
Default board is 9 x 6 inner corners.
```powershell
python main.py calibrate --input-dir data/calibration --output results/calibration/calibration.npz
```

### Stereo rectification
For a fully calibrated stereo camera setup, use the saved intrinsic/extrinsic parameters:
```powershell
python main.py rectify --left data/stereo/left.png --right data/stereo/right_resized.png --calibration results/calibration/stereo_calibration.npz
```

> Note: Accurate metric depth requires real camera intrinsics and a known stereo baseline. The demo stereo command supports focal length and baseline arguments; default values are demonstration parameters.

## Project structure
```text
Vision3D/
├── data/
├── results/
├── src/
│   ├── preprocessing.py
│   ├── features.py
│   ├── geometry.py
│   ├── segmentation.py
│   ├── calibration.py
│   └── stereo.py
├── tests/
├── main.py
├── statement.md
├── requirements.txt
└── .gitignore
```
