import RPi.GPIO as GPIO
import time

# GPIO 핀 번호 설정 (BCM 모드)
RELAY_PIN = 27

# GPIO 설정
GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY_PIN, GPIO.OUT)

def turn_on_humidifier():
    GPIO.output(RELAY_PIN, GPIO.HIGH)  # 릴레이 켜기
    print("Humidifier turned on")

def turn_off_humidifier():
    GPIO.output(RELAY_PIN, GPIO.LOW)  # 릴레이 끄기
    print("Humidifier turned off")

try:
    # 테스트 코드
    while True :
	    turn_on_humidifier()
	    time.sleep(5)  # 5초 동안 가습기 켜짐
	    turn_off_humidifier()
	    time.sleep(5)
finally:
    GPIO.cleanup()  # 모든 GPIO 설정 초기화

