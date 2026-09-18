import numpy as np
from src.stereo import disparity_to_depth, point_cloud_from_depth
def test_depth_formula():
    d=np.array([[10.,20.]])
    z=disparity_to_depth(d,700,0.1)
    assert np.allclose(z,[[7.,3.5]])
def test_point_cloud():
    depth=np.ones((10,10),np.float32)
    color=np.zeros((10,10,3),np.uint8)
    p=point_cloud_from_depth(depth,color,700)
    assert p.shape[1]==6
