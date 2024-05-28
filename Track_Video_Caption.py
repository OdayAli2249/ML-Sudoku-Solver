import cv2
import operator
import numpy as np
from Image_Processor import Merge_Two_Images

# Track Video Caption
def Track_Video_Caption(video_frame, current_solution):
    
    im = cv2.resize(video_frame, (500, 500))
    imGra = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    img = cv2.adaptiveThreshold(imGra, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 23, 12)
    imgt = cv2.bitwise_not(img, img)

    contor, hierarchy = cv2.findContours(imgt, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[-2:]

    contours = sorted(contor, key=cv2.contourArea, reverse=True)
    polygon = contours[0]
    bottom_right, _ = max(enumerate([pt[0][0] + pt[0][1] for pt in
                                     polygon]), key=operator.itemgetter(1))
    top_left, _ = min(enumerate([pt[0][0] + pt[0][1] for pt in
                                 polygon]), key=operator.itemgetter(1))
    bottom_left, _ = min(enumerate([pt[0][0] - pt[0][1] for pt in
                                    polygon]), key=operator.itemgetter(1))
    top_right, _ = max(enumerate([pt[0][0] - pt[0][1] for pt in
                                  polygon]), key=operator.itemgetter(1))

    Width, Height = 450, 450    # should be current solution dimension
    Width2, Height2 = 500, 500    # should be video frame dimension
    TransFrom = np.float32([[0, 0], [Height, 0], [0, Width], [Width, Height]])
    TransTo = np.float32([[polygon[top_left][0][0], polygon[top_left][0][1]],
                          [polygon[top_right][0][0], polygon[top_right][0][1]],
                          [polygon[bottom_left][0][0], polygon[bottom_left][0][1]],
                          [polygon[bottom_right][0][0], polygon[bottom_right][0][1]]])
    mat = cv2.getPerspectiveTransform(TransFrom, TransTo)
    imOut = cv2.warpPerspective(current_solution, mat, (Width2, Height2))

    terget_image = Merge_Two_Images(imOut, im)
    return terget_image