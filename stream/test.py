import cv2

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open camera")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    
    # 여기서 이미지 처리를 수행할 수 있습니다.
    # cv2.imshow('frame', frame) 대신 아래와 같이 이미지를 파일에 저장할 수도 있습니다.
    cv2.imwrite('frame.jpg', frame)
    
    # q 키를 눌러서 루프를 종료
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
