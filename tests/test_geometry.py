import numpy as np
from src.geometry import estimate_homography
def test_homography_identity():
    img=np.zeros((200,200,3),np.uint8)
    cv=__import__('cv2')
    cv.rectangle(img,(30,30),(170,170),(255,255,255),-1)
    H,mask,*_=estimate_homography(img,img)
    assert H.shape==(3,3)
    assert mask.dtype==bool
