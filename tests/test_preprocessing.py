import numpy as np, cv2
from src.preprocessing import grayscale, gaussian_blur, median_blur, histogram_equalization, canny_edges
def test_preprocessing_shapes():
    img=np.zeros((50,60,3),np.uint8)
    g=grayscale(img)
    assert g.shape==(50,60)
    assert gaussian_blur(g).shape==g.shape
    assert median_blur(g).shape==g.shape
    assert histogram_equalization(g).shape==g.shape
    assert canny_edges(g).shape==g.shape
