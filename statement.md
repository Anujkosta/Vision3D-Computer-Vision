# Project Statement — Vision3D

## Problem Statement
Computer Vision applications often require several processing stages such as enhancement, feature extraction, geometric matching, segmentation, depth estimation and 3D reconstruction. These stages are commonly implemented as separate experiments. Vision3D integrates them into one modular toolkit with reusable command-line modules and saved outputs.

## Scope
The project focuses on classical Computer Vision techniques from CSE3010. It accepts still images and stereo image pairs and produces intermediate visualizations, geometric results, depth maps and 3D point clouds.

## Target Users
- Computer Vision students
- Students performing CSE3010 experiments
- Developers learning classical image-processing and 3D-vision workflows

## High-Level Features
- Image enhancement and edge detection
- SIFT/Harris feature extraction and matching
- Homography estimation with RANSAC
- Multiple segmentation methods
- Chessboard camera calibration
- Stereo rectification support
- SGBM disparity and depth estimation
- PLY point-cloud generation
- CLI-based reproducible workflow

## Functional Requirements
FR-01: Load and validate image inputs.
FR-02: Perform preprocessing and enhancement.
FR-03: Extract and match local image features.
FR-04: Estimate homography using RANSAC.
FR-05: Perform image segmentation using selectable methods.
FR-06: Calibrate a camera from chessboard images.
FR-07: Rectify a stereo pair using calibration parameters.
FR-08: Estimate disparity/depth and generate a 3D point cloud.
FR-09: Save intermediate and final results.

## Non-Functional Requirements
NFR-01: Modularity — CV functions shall be separated into reusable source modules.
NFR-02: Reliability — invalid paths, unreadable images and incompatible dimensions shall produce clear errors.
NFR-03: Maintainability — source code shall use clear functions, docstrings and a predictable directory structure.
NFR-04: Usability — all major operations shall be accessible through documented CLI commands.
NFR-05: Portability — the toolkit shall run on systems supporting Python, NumPy and OpenCV.
NFR-06: Reproducibility — generated outputs shall be stored in the results directory.
