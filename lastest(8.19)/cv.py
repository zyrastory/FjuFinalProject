import numpy as np
import cv2


cap = cv2.VideoCapture(0)
count=0 

while(True):
   ret, frame = cap.read()
   cv2.imshow('frame.jpg',frame)
   cv2.imwrite('frame1.jpg', frame)
   count+=1

   if cv2.waitKey(5) & 0xFF == ord('q'):
       break

cap.release()
cv2.destroyAllWindows()