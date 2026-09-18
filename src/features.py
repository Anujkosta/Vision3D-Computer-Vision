from pathlib import Path
import cv2
from .preprocessing import load_image, grayscale, save

def harris_corners(gray, block_size=2, ksize=3, k=0.04):
    dst = cv2.cornerHarris(gray, block_size, ksize, k)
    return cv2.dilate(dst, None)

def create_sift():
    return cv2.SIFT_create()

def extract_sift(img):
    sift = create_sift()
    keypoints, descriptors = sift.detectAndCompute(grayscale(img), None)
    return keypoints, descriptors

def ratio_match(des1, des2, ratio=0.75):
    if des1 is None or des2 is None:
        return []
    matcher = cv2.BFMatcher(cv2.NORM_L2)
    pairs = matcher.knnMatch(des1, des2, k=2)
    return [m for m, n in pairs if m.distance < ratio*n.distance]

def run_features(image1, image2, output_dir="results/features"):
    out=Path(output_dir); out.mkdir(parents=True, exist_ok=True)
    a,b=load_image(image1),load_image(image2)
    k1,d1=extract_sift(a); k2,d2=extract_sift(b)
    good=ratio_match(d1,d2)
    vis=cv2.drawMatches(a,k1,b,k2,good,None,flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
    save(out/"01_sift_matches.png",vis)
    print(f"Image 1 keypoints: {len(k1)}")
    print(f"Image 2 keypoints: {len(k2)}")
    print(f"Good SIFT matches: {len(good)}")
