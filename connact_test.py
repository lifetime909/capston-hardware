import cv2

# 카메라 장치 열기 (0은 일반적으로 기본 카메라를 의미함)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("카메라를 열 수 없습니다")
    exit()

# 카메라로부터 한 프레임 읽기
ret, frame = cap.read()

if ret:
    # 프레임을 성공적으로 읽었다면 화면에 표시
    cv2.imshow('Camera Frame', frame)
    cv2.waitKey(0)  # 키 입력을 기다림
else:
    print("프레임을 읽을 수 없습니다")

# 카메라 장치 해제
cap.release()
