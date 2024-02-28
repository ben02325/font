import cv2
import datetime
from PIL import ImageFont, ImageDraw, Image
import numpy as np


capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

#글꼴 파일을 불러옴
font = ImageFont.truetype('fonts/SCDream5.otf', 20)


while True:
 #현재 시각을 불러와 문자열로 저장
  now = datetime.datetime.now()
  nowDatetime = now.strftime('%Y-%m-%d %H:%M:%S')

  ret, frame = capture.read() 
  #글자가 잘 보이도록 배경을 넣어줌
  #img는 사각형을 넣ㅇ르 이미지, pt1, pt2는 사각형의 시작점과 끝점, color는 색상(파랑, 초록, 빨강), thichness는 선굵기(-1은 내부를 채우는 것)
    
  
  cv2.rectangle(img=frame, pt1=(10, 15), pt2=(350, 35), color=(0,0,0), thickness=-1)

  #아래의 4줄은 글자를 영상에 더해주는 역할을 함
  frame = Image.fromarray(frame)
  draw = ImageDraw.Draw(frame)
  #xy는 택스트 시작위치, text는 출력할 문자열, font는 글꼴, font는 글꼴, fill은 글자색(파랑, 초록, 빨강)
  draw.text(xy=(10, 15), text="CCTV Monitor"+nowDatetime, font=font, fill=(255, 255, 255))
  frame = np.array(frame)

  cv2.imshow("text", frame) #현재 시간을 표시하는 글자를 써준 영상 출력
  if cv2.waitKey(1) == ord('q'): 
    break

capture.release() 
cv2.destroyAllWindows() 


