import argparse
from pathlib import Path
from src.preprocessing import run_preprocessing
from src.features import run_features
from src.geometry import run_homography
from src.segmentation import run_segmentation
from src.stereo import run_stereo
from src.calibration import run_calibration, run_rectification

def main():
    parser = argparse.ArgumentParser(description="Vision3D Computer Vision Toolkit")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("preprocess")
    p.add_argument("--input", required=True)
    p.add_argument("--output", default="results/preprocessing")

    p = sub.add_parser("features")
    p.add_argument("--image1", required=True)
    p.add_argument("--image2", required=True)
    p.add_argument("--output", default="results/features")

    p = sub.add_parser("homography")
    p.add_argument("--image1", required=True)
    p.add_argument("--image2", required=True)
    p.add_argument("--output", default="results/features")
    p.add_argument("--threshold", type=float, default=5.0)

    p = sub.add_parser("segment")
    p.add_argument("--input", required=True)
    p.add_argument("--output", default="results/segmentation")
    p.add_argument("--method", choices=["otsu", "edge", "region", "mean_shift", "all"], default="all")
    p.add_argument("--seed-x", type=int, default=None)
    p.add_argument("--seed-y", type=int, default=None)

    p = sub.add_parser("stereo")
    p.add_argument("--left", required=True)
    p.add_argument("--right", required=True)
    p.add_argument("--output", default="results/stereo")
    p.add_argument("--focal-length", type=float, default=700.0)
    p.add_argument("--baseline", type=float, default=0.10)
    p.add_argument("--num-disparities", type=int, default=128)
    p.add_argument("--block-size", type=int, default=5)

    p = sub.add_parser("calibrate")
    p.add_argument("--input-dir", required=True)
    p.add_argument("--output", default="results/calibration/camera_calibration.npz")
    p.add_argument("--columns", type=int, default=9)
    p.add_argument("--rows", type=int, default=6)
    p.add_argument("--square-size", type=float, default=1.0)

    p = sub.add_parser("rectify")
    p.add_argument("--left", required=True)
    p.add_argument("--right", required=True)
    p.add_argument("--calibration", required=True)
    p.add_argument("--output", default="results/calibration")

    args = parser.parse_args()

    if args.command == "preprocess":
        run_preprocessing(args.input, args.output)
    elif args.command == "features":
        run_features(args.image1, args.image2, args.output)
    elif args.command == "homography":
        run_homography(args.image1, args.image2, args.output, args.threshold)
    elif args.command == "segment":
        run_segmentation(args.input, args.output, args.method, args.seed_x, args.seed_y)
    elif args.command == "stereo":
        run_stereo(args.left, args.right, args.output, args.focal_length, args.baseline,
                   args.num_disparities, args.block_size)
    elif args.command == "calibrate":
        run_calibration(args.input_dir, args.output, (args.columns, args.rows), args.square_size)
    elif args.command == "rectify":
        run_rectification(args.left, args.right, args.calibration, args.output)

if __name__ == "__main__":
    main()
