import cv2
from PIL import ImageFont, ImageDraw, Image
import numpy as np
import os
import datetime

capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

is_record = False                           
on_record = False
cnt_record = 0      
max_cnt_record = 5  

fourcc = cv2.VideoWriter_fourcc(*'XVID')    
font = ImageFont.truetype('fonts/SCDream5.otf', 20) 

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade/haarcascade_eye_tree_eyeglasses.xml')

while True:
   
    now = datetime.datetime.now()
    nowDatetime = now.strftime('%Y-%m-%d %H:%M:%S')
    nowDatetime_path = now.strftime('%Y-%m-%d %H_%M_%S') 

    ret, frame = capture.read()     
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  
    
    cv2.rectangle(img=frame, pt1=(10, 15), pt2=(340, 35), color=(0,0,0), thickness=-1)     
    frame = Image.fromarray(frame)    
    draw = ImageDraw.Draw(frame)    
      
    draw.text(xy=(10, 15),  text="CCTV "+nowDatetime, font=font, fill=(255, 255, 255))
    frame = np.array(frame)
    
    faces = face_cascade.detectMultiScale(gray, scaleFactor= 1.5, minNeighbors=3, minSize=(20,20))
    print(faces)
    
    if len(faces) :
        is_record = True   
        if on_record == False:
            video = cv2.VideoWriter("capture/face " + nowDatetime_path + ".avi", fourcc, 1, (frame.shape[1], frame.shape[0]))
        cnt_record = max_cnt_record
        
    if is_record == True:   
        print('녹화 중')
        video.write(frame)    
        cnt_record -= 1    
        on_record = True   
    if cnt_record == 0:     
        is_record = False   
        on_record = False
    
    if len(faces) :
        for  x, y, w, h in faces :
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255,255,255), 2, cv2.LINE_4)
    cv2.imshow("original", frame)   
    if cv2.waitKey(1000) == ord('q'):  
            break

capture.release()                  
cv2.destroyAllWindows()  
           