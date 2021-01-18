import cv2
import numpy as np
cap=cv2.VideoCapture(1)
while True:
    ret,frame=cap.read()
    cv2.imshow("frame",frame)
    img=cap.read()
    if cv2.waitKey(1) & 0xFF==ord('q'):
        img=cv2.imwrite('/home/pi/Desktop/wastesort/test/image.jpg',frame)
        break
cap.release()
cv2.destoryALLWindows()
 
