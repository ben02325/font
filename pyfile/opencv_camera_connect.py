import cv2

# 카메라 연결
capture = cv2.VideoCapture(0)
# 프레임 너비 설정
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
# 프레임 높이 설정
capture.set(cv2.CAP_PROP_FRAME_HEIGHT,720)

# 무한 반복하여 프레임 표시
while True:
    # 프레임 읽기
    ret, frame = capture.read()
    # 원본 프레임 출력
    cv2.imshow("원본", frame)
    # 'q' 키를 눌러 종료
    if cv2.waitKey(1) == ord('q'):
        break
    
# 카메라 연결 해제
capture.release()
