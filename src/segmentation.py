from pathlib import Path
import cv2
import numpy as np
from .preprocessing import load_image, grayscale, save

def otsu_segmentation(gray):
    _, mask = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    return mask

def edge_segmentation(gray):
    return cv2.Canny(gray, 100, 200)

def region_growing(gray, seed, threshold=12):
    h,w=gray.shape
    sx,sy=seed
    if not (0<=sx<w and 0<=sy<h): raise ValueError("Seed is outside image.")
    visited=np.zeros((h,w),np.uint8)
    mask=np.zeros((h,w),np.uint8)
    from collections import deque
    q=deque([(sx,sy)])
    seed_value=int(gray[sy,sx])
    while q:
        x,y=q.popleft()
        if visited[y,x]: continue
        visited[y,x]=1
        if abs(int(gray[y,x])-seed_value)<=threshold:
            mask[y,x]=255
            for nx,ny in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)):
                if 0<=nx<w and 0<=ny<h and not visited[ny,nx]:
                    q.append((nx,ny))
    return mask

def mean_shift_segmentation(img, spatial=15, color=30):
    return cv2.pyrMeanShiftFiltering(img, spatial, color)

def run_segmentation(input_path, output_dir="results/segmentation", method="all",
                     seed_x=None, seed_y=None):
    out=Path(output_dir);out.mkdir(parents=True,exist_ok=True)
    img=load_image(input_path); gray=grayscale(img)
    methods=["otsu","edge","region","mean_shift"] if method=="all" else [method]
    for m in methods:
        if m=="otsu": result=otsu_segmentation(gray)
        elif m=="edge": result=edge_segmentation(gray)
        elif m=="region":
            sx=gray.shape[1]//2 if seed_x is None else seed_x
            sy=gray.shape[0]//2 if seed_y is None else seed_y
            result=region_growing(gray,(sx,sy))
        else: result=mean_shift_segmentation(img)
        save(out/f"{m}.png",result)
    print(f"Segmentation completed ({', '.join(methods)}). Results: {out.resolve()}")
