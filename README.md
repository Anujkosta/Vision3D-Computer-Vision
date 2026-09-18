# Vision3D — Modular Computer Vision Toolkit

Vision3D is a modular Computer Vision toolkit developed for the **CSE3010 Computer Vision** course. The project provides a command-line interface for performing image preprocessing, feature extraction and matching, projective geometry, image segmentation, camera calibration support, stereo depth estimation, and 3D point-cloud reconstruction.

## Features

- Image preprocessing and enhancement
- Harris corner detection
- SIFT feature extraction
- Feature matching using BFMatcher
- Lowe's ratio test
- Homography estimation
- RANSAC-based robust estimation
- Perspective image warping
- Otsu thresholding
- Edge-based segmentation
- Region growing
- Mean-shift segmentation
- Camera calibration support
- Stereo rectification support
- Stereo disparity estimation using SGBM
- Depth estimation from stereo images
- 3D point-cloud generation
- PLY point-cloud export
- Automated testing using pytest

## Modules

### 1. Image Preprocessing

Performs basic image enhancement and low-level processing:

- Grayscale conversion
- Gaussian filtering
- Median filtering
- Histogram equalization
- Canny edge detection

Run:

```bash
python main.py preprocess --input data/input/sample.jpg
```

Results are saved in:

```text
results/preprocessing/
```

### 2. Feature Extraction and Matching

Extracts and matches visual features between two images using:

- Harris corner detection
- SIFT descriptors
- Brute-Force Matcher
- Lowe's ratio test

Run:

```bash
python main.py features --image1 data/input/sample.jpg --image2 data/input/image2.jpg
```

Results are saved in:

```text
results/features/
```

### 3. Homography and RANSAC

Estimates a projective transformation between two images using matched feature points.

The module uses:

- Homography estimation
- RANSAC
- Inlier detection
- Perspective transformation

Run:

```bash
python main.py homography --image1 data/input/sample.jpg --image2 data/input/image2.jpg
```

The program reports:

- Total good matches
- RANSAC inliers
- Inlier ratio
- Homography matrix

### 4. Image Segmentation

Vision3D supports multiple segmentation approaches:

- Otsu thresholding
- Edge-based segmentation
- Region growing
- Mean-shift segmentation

Run all methods:

```bash
python main.py segment --input data/input/sample.jpg --method all
```

Individual methods can also be selected:

```bash
python main.py segment --input data/input/sample.jpg --method otsu
```

```bash
python main.py segment --input data/input/sample.jpg --method edge
```

```bash
python main.py segment --input data/input/sample.jpg --method region
```

```bash
python main.py segment --input data/input/sample.jpg --method mean_shift
```

Results are saved in:

```text
results/segmentation/
```

### 5. Camera Calibration

The project includes support for camera calibration using chessboard images.

Calibration images should be placed in:

```text
data/calibration/
```

Calibration can be run using:

```bash
python main.py calibrate --input-dir data/calibration --output results/calibration/calibration.npz
```

> Camera calibration requires suitable chessboard calibration images.

### 6. Stereo Depth Estimation and 3D Reconstruction

The stereo module estimates depth from a left-right image pair using **Semi-Global Block Matching (SGBM)**.

Processing includes:

1. Stereo image loading
2. Disparity estimation
3. Disparity normalization
4. Depth calculation
5. 3D point-cloud generation
6. PLY export

The stereo images should have the same dimensions and should ideally be rectified or horizontally aligned.

Run:

```bash
python main.py stereo --left data/stereo/left.png --right data/stereo/right_resized.png
```

Results are saved in:

```text
results/stereo/
```

Generated outputs include:

```text
01_disparity.png
02_disparity_colormap.png
03_depth_map.png
04_point_cloud.ply
```

### Depth Calculation

Depth is estimated using:

```text
Z = (f × B) / d
```

where:

- `Z` = estimated depth
- `f` = camera focal length
- `B` = stereo baseline
- `d` = disparity

Custom focal length and baseline can be supplied:

```bash
python main.py stereo --left data/stereo/left.png --right data/stereo/right_resized.png --focal-length 700 --baseline 0.10
```

> Accurate metric depth requires real camera calibration parameters and a known stereo baseline. Default parameters are demonstration values.

## Technologies Used

- **Python**
- **OpenCV**
- **NumPy**
- **Pytest**

## Project Structure

```text
Vision3D/
│
├── data/
│   ├── input/
│   ├── stereo/
│   └── calibration/
│
├── results/
│   ├── preprocessing/
│   ├── features/
│   ├── segmentation/
│   ├── stereo/
│   └── calibration/
│
├── src/
│   ├── __init__.py
│   ├── preprocessing.py
│   ├── features.py
│   ├── geometry.py
│   ├── segmentation.py
│   ├── calibration.py
│   └── stereo.py
│
├── tests/
│   ├── __init__.py
│   ├── test_preprocessing.py
│   ├── test_features.py
│   ├── test_geometry.py
│   ├── test_segmentation.py
│   └── test_stereo.py
│
├── main.py
├── requirements.txt
├── statement.md
└── .gitignore
```

## Installation

### Prerequisites

- Python 3.10 or higher
- pip

### Create Virtual Environment

Windows PowerShell:

```powershell
python -m venv .venv
```

Activate it:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

## Testing

Vision3D includes automated tests using `pytest`.

Run:

```bash
pytest -q
```

Current local test result:

```text
9 passed
```

The tests cover:

- Image preprocessing
- Feature processing
- Projective geometry
- Image segmentation
- Stereo processing

## Example Results

The project generates visual outputs such as:

- Enhanced images
- Canny edge maps
- Feature matching visualizations
- RANSAC inlier visualizations
- Segmentation masks
- Stereo disparity maps
- Depth maps
- 3D point clouds

All generated results are organized inside the `results/` directory.

## Computer Vision Concepts

Vision3D demonstrates several concepts from the CSE3010 Computer Vision syllabus:

- Image formation and preprocessing
- Image enhancement
- Convolution and filtering
- Histogram processing
- Edge detection
- Feature extraction
- Feature matching
- Homography
- RANSAC
- Image segmentation
- Camera calibration
- Stereo vision
- Depth estimation
- 3D reconstruction

## Limitations

- Stereo depth quality depends on image alignment, camera parameters, disparity estimation, and image quality.
- The demonstration stereo workflow assumes a rectified or horizontally aligned stereo pair.
- Metric depth is dependent on accurate focal length and baseline values.
- Camera calibration requires suitable chessboard images.

## Future Enhancements

- Automatic stereo calibration
- Improved stereo matching
- Dense 3D reconstruction
- Interactive 3D point-cloud visualization
- Object detection
- Object tracking
- Optical flow analysis
- Additional feature descriptors
- Web-based graphical interface

## Academic Project

This project was developed as a **Build Your Own Project** for:

**CSE3010 — Computer Vision**

The project integrates multiple Computer Vision techniques into a single modular toolkit.

## Author

**Anuj Kosta**

Computer Science and Engineering  
Artificial Intelligence and Machine Learning

## License

This project is intended for academic and educational purposes.
