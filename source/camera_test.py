import cv2

capture = cv2.VideoCapture(0)

if not capture.isOpened():
    print("카메라를 열 수 없습니다.")
    exit()

while True:
    ret, frame = capture.read()
    if not ret:
        print("프레임을 읽을 수 없습니다.")
        break

    # 화면에 이미지를 출력하지 않고 단순히 프레임을 읽어서 확인
    print("프레임을 성공적으로 읽어왔습니다.")
    # 'q' 키를 누르면 루프를 종료합니다.
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()
