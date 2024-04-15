import cv2
import datetime

# 카메라 설정
cap = cv2.VideoCapture(0)  # 0은 첫 번째 카메라를 의미합니다.
fourcc = cv2.VideoWriter_fourcc(*'XVID')  # 동영상 포맷 설정
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

def get_video_writer():
    now = datetime.datetime.now()
    filename = now.strftime('%Y-%m-%d_%H-%M-%S.avi')  # 파일 이름에 현재 시간을 포함
    return cv2.VideoWriter(filename, fourcc, 20.0, (frame_width, frame_height))

# 현재 시간을 기준으로 첫 번째 비디오 파일 생성
video_writer = get_video_writer()
start_time = datetime.datetime.now()

while(True):
    ret, frame = cap.read()  # 카메라로부터 이미지 읽기
    if ret:
        video_writer.write(frame)  # 이미지를 비디오 파일에 쓰기

        # 현재 시간 가져오기
        now = datetime.datetime.now()
        # 시작 시간으로부터 1시간이 지났는지 확인
        if (now - start_time).seconds > 3600:
            video_writer.release()  # 현재 비디오 파일 저장 완료
            video_writer = get_video_writer()  # 새로운 비디오 파일 생성
            start_time = now  # 시작 시간 업데이트
    else:
        break

# 모든 자원 해제
cap.release()
video_writer.release()
cv2.destroyAllWindows()

