import numpy as np
from src.segmentation import otsu_segmentation, edge_segmentation, region_growing
def test_otsu_shape():
    img=np.zeros((40,50),np.uint8); img[:,25:]=255
    assert otsu_segmentation(img).shape==img.shape
def test_edge_shape():
    img=np.zeros((40,50),np.uint8)
    assert edge_segmentation(img).shape==img.shape
def test_region_shape():
    img=np.full((30,30),100,np.uint8)
    assert region_growing(img,(15,15)).shape==img.shape
