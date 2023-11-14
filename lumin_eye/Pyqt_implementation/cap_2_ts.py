import numpy as np
import cv2
import datetime
import os

cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)

path_folder = 'C:\\Users\\Biancaa. R\\lumin_eye\\saved'
os.chdir(path_folder)
fourcc = cv2.VideoWriter_fourcc(*'MP4V') #MP4V codec,
#ts=str(datetime.datetime.now())
#path='C:\\Users\\Biancaa. R\\lumin_eye\\saved\\output_{}.mp4'.format(ts)
#path='output_'+ts+'.mp4'
ts = (datetime.datetime.now()).strftime("%Y_%m_%d_%H_%M_%S")
path = 'C:\\Users\\Biancaa. R\\lumin_eye\\saved\\output_{}.mp4'.format(ts)
print(path)
out = cv2.VideoWriter(path, fourcc, 10.0, (640,480))
while(True):
    ret, frame = cap.read()
    out.write(frame)
    cv2.imshow('frame', frame)
    #c = cv2.waitKey(1)
    #if c & 0xFF == ord('q'):
    if cv2.waitKey(1)==ord('q'): 
        break

cap.release()
out.release() #closes the output video file
cv2.destroyAllWindows()