import cv2
import datetime
from PIL import ImageFont, ImageDraw, Image
import numpy as np
import os


def get_diff_img(frame_a, frame_b, frame_c, threshold):
    
    frame_a_gray = cv2.cvtColor(frame_a, cv2.COLOR_BGR2GRAY)
    frame_b_gray = cv2.cvtColor(frame_b, cv2.COLOR_BGR2GRAY)
    frame_c_gray = cv2.cvtColor(frame_c, cv2.COLOR_BGR2GRAY)

    diff_ab = cv2.absdiff(frame_a_gray, frame_b_gray)
    diff_bc = cv2.absdiff(frame_b_gray, frame_c_gray)

    ret, diff_ab_t = cv2.threshold(diff_ab, threshold, 255, cv2.THRESH_BINARY)
    ret, diff_bc_t = cv2.threshold(diff_bc, threshold, 255, cv2.THRESH_BINARY)

    diff = cv2.bitwise_and(diff_ab_t, diff_bc_t)
    
    k = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
    diff = cv2.morphologyEx(diff, cv2.MORPH_OPEN, k)

    diff_cnt = cv2.countNonZero(diff)
    return diff, diff_cnt
    

capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

fourcc = cv2.VideoWriter_fourcc(*'XVID')    
font = ImageFont.truetype('fonts/SCDream5.otf', 20) 
is_record = False                           
on_record = False

threshold = 40      
diff_max = 10       
cnt_record = 0      
max_cnt_record = 5  

ret, frame_a = capture.read()
ret, frame_b = capture.read()

while True:
    
    now = datetime.datetime.now()
    nowDatetime = now.strftime('%Y-%m-%d %H:%M:%S')
    nowDatetime_path = now.strftime('%Y-%m-%d %H_%M_%S') 

    ret, frame_c = capture.read()
    diff, diff_cnt = get_diff_img(frame_a=frame_a, frame_b=frame_b, frame_c=frame_c, threshold=threshold)
    
    if diff_cnt > diff_max:
        is_record = True    
        if on_record == False:
            video = cv2.VideoWriter("capture/moving " + nowDatetime_path + ".avi", fourcc, 1, (frame_c.shape[1], frame_c.shape[0]))
        cnt_record = max_cnt_record
    if is_record == True:   
        print('녹화 중')
        video.write(frame_c)    
        cnt_record -= 1     
        on_record = True    
    if cnt_record == 0:     
        is_record = False  
        on_record = False
    
    cv2.imshow("diff", diff)
    frame = np.array(frame_c)
    
    cv2.rectangle(img=frame, pt1=(10, 15), pt2=(340, 35), color=(0,0,0), thickness=-1)     
    
    frame = Image.fromarray(frame)    
    draw = ImageDraw.Draw(frame)    
       
    draw.text(xy=(10, 15),  text="CCTV "+nowDatetime, font=font, fill=(255, 255, 255))
    frame = np.array(frame)
    frame_a = np.array(frame_b)
    frame_b = np.array(frame_c)

    key = cv2.waitKey(1000)       
    if key == ord('q'):  
            break
    cv2.imshow("original", frame)   
    
capture.release()                   
cv2.destroyAllWindows()            