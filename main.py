import cv2
from Solution_Pipline import Solution_Pipline
from Track_Video_Caption import Track_Video_Caption
from ML_Model import new_model

# Video Capture
import time
model = new_model
OCR_VERSION = 1
LOD = []
cap = cv2.VideoCapture(0)
for i in range(0,10):
    LOD.append(cv2.imread('Resources/digits/d' + str(i) +'.jpg',0))
timestamp = int(time.time() * 1000.0)
counter = 0
_, frame = cap.read()
sol,im = Solution_Pipline(frame,model,LOD,OCR_VERSION)
while True:
     _, frame = cap.read()
     print(counter)
     counter +=1
     timestamp1 = int(time.time() * 1000.0)
     if(counter > 50):
        sol,im = Solution_Pipline(frame,model,LOD,OCR_VERSION)
        counter = 0
     else:
        im = Track_Video_Caption(frame,sol)
     timestamp2 = int(time.time() * 1000.0)
     print('bet two frames  ',timestamp2 - timestamp1)
     print('until now  ',timestamp2 - timestamp)
     cv2.imshow(' Video ', im)
     key = cv2.waitKey(1)
     if key == 7:
         break


