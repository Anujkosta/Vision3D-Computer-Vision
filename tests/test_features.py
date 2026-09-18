import numpy as np
from src.features import extract_sift, ratio_match

def test_sift_runs():
    img=np.random.randint(0,256,(150,150,3),np.uint8)
    k,d=extract_sift(img)
    assert k is not None
    assert d is None or d.ndim == 2

def test_ratio_empty():
    assert ratio_match(None,None)==[]
