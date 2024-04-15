import time
import board
import adafruit_dht

# GPIO 핀 번호를 board 모듈을 사용하여 지정
pin = board.D4  # GPIO 4번 핀 사용

# 센서 객체 초기화
dhtDevice = adafruit_dht.DHT11(pin)

while True:
    try:
        # 센서로부터 온도와 습도값 읽기
        temperature = dhtDevice.temperature
        humidity = dhtDevice.humidity

        # 온도와 습도 출력
        print("Temp : ", temperature)
        print("Humi : ", humidity)

        # 2초 대기
        time.sleep(2)

    except RuntimeError as error:  # 런타임 오류 예외처리
        print(error.args[0])

    except KeyboardInterrupt:  # 키보드 인터럽트 예외처리
        break

# 사용이 끝난 후 센서 객체 정리
dhtDevice.exit()
