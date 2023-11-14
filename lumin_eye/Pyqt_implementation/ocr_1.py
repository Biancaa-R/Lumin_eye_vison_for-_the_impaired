import pytesseract
import cv2
from PIL import Image
import os
pytesseract.pytesseract.tesseract_cmd=r'D:\tesseract\tesseract.exe'
cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)

import time
vid=False

while(True):
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame")
        break
    cv2.imshow('frame', frame)
    #we cannot pass img direct

    scanned_text = pytesseract.image_to_string(Image.fromarray(frame))
    scanned_text=scanned_text[:-2] #STORES TEXT
    print(scanned_text)
    #OUTPUT DIRECTORY FOR TEXT FILE STORAGE

    out_file = open("output.txt" , "w+") 
    out_file.write(scanned_text)
    
    #c = cv2.waitKey(1)
    #if c & 0xFF == ord('q'):
    if cv2.waitKey(1)==ord('q') and vid==True: 
        break
    
cap.release()
cv2.destroyAllWindows()
