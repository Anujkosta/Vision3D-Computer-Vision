from pathlib import Path
import cv2
import numpy as np
from .preprocessing import load_image, save

def calibrate_camera(image_paths, pattern_size=(9,6), square_size=1.0):
    cols,rows=pattern_size
    objp=np.zeros((rows*cols,3),np.float32)
    objp[:,:2]=np.mgrid[0:cols,0:rows].T.reshape(-1,2)*square_size
    objpoints=[]; imgpoints=[]; image_size=None
    for path in image_paths:
        img=load_image(path); gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        image_size=(gray.shape[1],gray.shape[0])
        found,corners=cv2.findChessboardCorners(gray,pattern_size,None)
        if found:
            corners=cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),
                                     (cv2.TERM_CRITERIA_EPS+cv2.TERM_CRITERIA_MAX_ITER,30,0.001))
            objpoints.append(objp); imgpoints.append(corners)
    if not objpoints: raise ValueError("No chessboard corners found. Need calibration images.")
    rms,K,dist,rvecs,tvecs=cv2.calibrateCamera(objpoints,imgpoints,image_size,None,None)
    return rms,K,dist,rvecs,tvecs,len(objpoints),image_size

def run_calibration(input_dir, output_path, pattern_size=(9,6), square_size=1.0):
    paths=sorted([p for p in Path(input_dir).glob("*") if p.suffix.lower() in {".jpg",".jpeg",".png",".bmp"}])
    if not paths: raise FileNotFoundError(f"No calibration images found in {input_dir}")
    rms,K,dist,rvecs,tvecs,count,size=calibrate_camera(paths,pattern_size,square_size)
    Path(output_path).parent.mkdir(parents=True,exist_ok=True)
    np.savez(output_path,camera_matrix=K,dist_coeffs=dist,rms=rms,
             image_width=size[0],image_height=size[1],valid_images=count)
    print(f"Calibration completed using {count} valid images.")
    print(f"RMS reprojection error: {rms:.4f}")
    print(f"Saved: {Path(output_path).resolve()}")

def rectify_pair(left_path,right_path,calibration_path,output_dir):
    left=load_image(left_path); right=load_image(right_path)
    if left.shape[:2]!=right.shape[:2]: raise ValueError("Left and right images must have the same dimensions.")
    data=np.load(calibration_path)
    K=data["camera_matrix"]; dist=data["dist_coeffs"]
    size=(left.shape[1],left.shape[0])
    # Single-camera undistortion/rectification. True stereo rectification additionally needs
    # a calibrated R and T between two cameras.
    map1x,map1y=cv2.initUndistortRectifyMap(K,dist,None,K,size,cv2.CV_32FC1)
    map2x,map2y=map1x,map1y
    rl=cv2.remap(left,map1x,map1y,cv2.INTER_LINEAR)
    rr=cv2.remap(right,map2x,map2y,cv2.INTER_LINEAR)
    out=Path(output_dir);out.mkdir(parents=True,exist_ok=True)
    save(out/"rectified_left.png",rl); save(out/"rectified_right.png",rr)
    print(f"Rectification/undistortion completed. Results: {out.resolve()}")

def run_rectification(left,right,calibration,output): rectify_pair(left,right,calibration,output)
