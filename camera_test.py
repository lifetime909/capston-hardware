import cv2
import time

# 카메라 인덱스를 변경해가며 시도해보세요.
cap = cv2.VideoCapture(0)  # 또는 1, 2 등 다른 숫자로 변경

# 카메라 초기화를 위해 잠시 대기
time.sleep(2)

if not cap.isOpened():
    print("카메라를 열 수 없습니다.")
else:
    # 카메라로부터 한 프레임 읽기 시도
    ret, frame = cap.read()

    if ret:
        # 'captured_image.jpg'라는 이름으로 이미지 저장
        cv2.imwrite('captured_image.jpg', frame)
        print("이미지 저장 성공")
    else:
        print("카메라로부터 이미지를 읽을 수 없습니다.")

    # 작업이 끝났으므로, 카메라 장치를 해제
    cap.release()

