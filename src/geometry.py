from pathlib import Path
import cv2
import numpy as np
from .preprocessing import load_image, save
from .features import extract_sift, ratio_match

def estimate_homography(img1, img2, ransac_threshold=5.0):
    k1,d1=extract_sift(img1); k2,d2=extract_sift(img2)
    good=ratio_match(d1,d2)
    if len(good)<4:
        raise ValueError("At least 4 good matches are required for homography.")
    src=np.float32([k1[m.queryIdx].pt for m in good]).reshape(-1,1,2)
    dst=np.float32([k2[m.trainIdx].pt for m in good]).reshape(-1,1,2)
    H,mask=cv2.findHomography(src,dst,cv2.RANSAC,ransac_threshold)
    if H is None or mask is None: raise ValueError("Homography estimation failed.")
    return H,mask.ravel().astype(bool),k1,k2,good

def run_homography(image1,image2,output_dir="results/features",threshold=5.0):
    out=Path(output_dir);out.mkdir(parents=True,exist_ok=True)
    a,b=load_image(image1),load_image(image2)
    H,inliers,k1,k2,good=estimate_homography(a,b,threshold)
    inlier_matches=[m for m,keep in zip(good,inliers) if keep]
    vis=cv2.drawMatches(a,k1,b,k2,inlier_matches,None,flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
    save(out/"02_ransac_inliers.png",vis)
    np.savetxt(out/"homography_matrix.txt",H,fmt="%.8f")
    print(f"Total good matches: {len(good)}")
    print(f"RANSAC inliers: {int(inliers.sum())}")
    print(f"Inlier ratio: {100*inliers.mean():.2f}%")
    print("Homography matrix:")
    print(H)

def warp_perspective(img,H,size): return cv2.warpPerspective(img,H,size)
