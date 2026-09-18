from pathlib import Path
import cv2
import numpy as np
from .preprocessing import load_image, save

def compute_disparity(left,right,num_disparities=128,block_size=5):
    if num_disparities%16!=0: raise ValueError("num_disparities must be divisible by 16.")
    if block_size%2==0 or block_size<3: raise ValueError("block_size must be odd and >= 3.")
    g1=cv2.cvtColor(left,cv2.COLOR_BGR2GRAY); g2=cv2.cvtColor(right,cv2.COLOR_BGR2GRAY)
    matcher=cv2.StereoSGBM_create(minDisparity=0,numDisparities=num_disparities,
        blockSize=block_size,P1=8*block_size**2,P2=32*block_size**2,
        uniquenessRatio=10,speckleWindowSize=100,speckleRange=2,
        disp12MaxDiff=1,mode=cv2.STEREO_SGBM_MODE_SGBM_3WAY)
    return matcher.compute(g1,g2).astype(np.float32)/16.0

def disparity_to_depth(disparity,focal_length,baseline):
    d=np.maximum(disparity,1e-6)
    depth=(focal_length*baseline)/d
    depth[disparity<=0]=0
    return depth

def point_cloud_from_depth(depth, color, focal_length):
    h,w=depth.shape
    cx,cy=w/2.0,h/2.0
    ys,xs=np.where(depth>0)
    z=depth[ys,xs]; x=(xs-cx)*z/focal_length; y=(ys-cy)*z/focal_length
    rgb=color[ys,xs][:,::-1]
    return np.column_stack((x,y,z,rgb))

def save_ply(path,points):
    Path(path).parent.mkdir(parents=True,exist_ok=True)
    with open(path,"w",encoding="utf-8") as f:
        f.write("ply\nformat ascii 1.0\n")
        f.write(f"element vertex {len(points)}\n")
        f.write("property float x\nproperty float y\nproperty float z\n")
        f.write("property uchar red\nproperty uchar green\nproperty uchar blue\nend_header\n")
        for p in points:
            f.write(f"{p[0]:.6f} {p[1]:.6f} {p[2]:.6f} {int(p[3])} {int(p[4])} {int(p[5])}\n")

def run_stereo(left_path,right_path,output_dir="results/stereo",focal_length=700.0,
               baseline=0.10,num_disparities=128,block_size=5):
    out=Path(output_dir);out.mkdir(parents=True,exist_ok=True)
    left,right=load_image(left_path),load_image(right_path)
    if left.shape[:2]!=right.shape[:2]: raise ValueError("Left and right images must have the same dimensions")
    disp=compute_disparity(left,right,num_disparities,block_size)
    valid=disp>0
    if not np.any(valid): raise ValueError("No valid disparity pixels were produced.")
    dnorm=cv2.normalize(disp,None,0,255,cv2.NORM_MINMAX).astype(np.uint8)
    color=cv2.applyColorMap(dnorm,cv2.COLORMAP_JET)
    depth=disparity_to_depth(disp,focal_length,baseline)
    depth_vis=cv2.normalize(depth,None,0,255,cv2.NORM_MINMAX).astype(np.uint8)
    points=point_cloud_from_depth(depth,left,focal_length)
    save(out/"01_disparity.png",dnorm); save(out/"02_disparity_colormap.png",color)
    save(out/"03_depth_map.png",depth_vis); save_ply(out/"04_point_cloud.ply",points)
    print("Vision3D stereo depth estimation completed.")
    print(f"Valid depth pixels : {int(valid.sum())}")
    print(f"Point cloud points : {len(points)}")
    print(f"Median depth       : {float(np.median(depth[valid])):.3f} m")
    print(f"Results            : {out.resolve()}")
