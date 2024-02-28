import cv2
import datetime
from PIL import ImageFont, ImageDraw, Image
import numpy as np


capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

fourcc = cv2.VideoWriter_fourcc(*'XVID') #영상을 기록할 코덱 설정
font = ImageFont.truetype('fonts/SCDream6.otf', 20) #글꼴 파일을 불러옴
is_record = False #녹화 상태는 처음엔 거짓으로 설정

while True:
#현재 시각을 불러와 문자열로 저장
  now = datetime.datetime.now()
  nowDatetime = now.strftime('%Y-%m-%d %H:%M:%S')
  nowDatetime_path = now.strftime('%Y-%m-%d %H_%M_%S') #파일 이름으로는 :를 못쓰기 때문에 따로 만들어줌
  ret, frame = capture.read() 

  cv2.rectangle(img=frame, pt1=(10, 15), pt2=(340, 35), color=(0,0,0), thickness=-1)

  frame = Image.fromarray(frame)
  draw = ImageDraw.Draw(frame)
  
  draw.text(xy=(10, 15), text="CCTV "+nowDatetime, font=font, fill=(255, 255, 255))
  frame = np.array(frame)


  key = cv2.waitKey(30) #30ms동안 키입력 대기
  if key == ord('r') and is_record == False: #현재 녹화상태가 아니며 r키를 누르면
    is_record = True #녹화상태로 만들어줌
   #비디오 객체에 (파일이름(한글가능), 인코더, 초당프레임률(정확하지 않음), 영상크기) 로 영상을 쏠 준비
    video = cv2.VideoWriter("capture/recording " + nowDatetime_path + ".avi", fourcc, 15, (frame.shape[1], frame.shape[0]))
  elif key == ord('r') and is_record == True: 
    is_record = False 
    video.release() 
  elif key == ord('c'): 
    
    cv2.imwrite("capture/capture " + nowDatetime_path + ".png", frame) 
  elif key == ord('q'): 
      break
  if is_record == True: 
    
    video.write(frame)
    
    cv2.circle(img=frame, center=(620, 15), radius=5, color=(0,0,255), thickness=-1)
  cv2.imshow("output", frame) 

capture.release() 
cv2.destroyAllWindows() 