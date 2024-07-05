import RPi.GPIO as GPIO
import time
import pigpio
import json
import board
import adafruit_dht

# GPIO 핀 번호 설정
HUM_PIN = 27
LEMP_PIN = 22
FAN_PIN = 18
DHT_PIN = board.D17

# 수정된 부분: GPIO 설정 추가
GPIO.setmode(GPIO.BCM)
GPIO.setup(HUM_PIN, GPIO.OUT)
GPIO.setup(LEMP_PIN, GPIO.OUT)

# FAN 연결
pi = pigpio.pi()
if not pi.connected:
    exit()

# PWM 주파수 설정
pi.set_PWM_frequency(FAN_PIN, 25000)

# DHT22 센서 초기화
dhtDevice = adafruit_dht.DHT22(DHT_PIN)

#가습기 모듈 On
def turn_on_humidifier():
    GPIO.output(HUM_PIN, GPIO.HIGH)  # 릴레이 켜기
    print("Humidifier turned on")

#가습기 모듈 Off
def turn_off_humidifier():
    GPIO.output(HUM_PIN, GPIO.LOW)  # 릴레이 끄기
    print("Humidifier turned off")

# LED 모듈 On
def turn_on_lemp():
    GPIO.output(LEMP_PIN, GPIO.HIGH)  # 릴레이 켜기
    print("Lemp turned on")

# LED 모듈 Off
def turn_off_lemp():
    GPIO.output(LEMP_PIN, GPIO.LOW)  # 릴레이 끄기
    print("Lemp turned off")

try:
    while True:
        try:
            # data.json 읽기
            with open('data.json', 'r', encoding='utf-8') as file:
                data = json.load(file)

            # 온도와 습도 데이터 사용
            set_temperature = data["temperature"]
            set_humidity = data["humidity"]

            # DHT22 센서 데이터 측정
            temperature = dhtDevice.temperature
            humidity = dhtDevice.humidity

            print(f"Measured Temperature: {temperature}°C, Humidity: {humidity}%")
            print(f"Measured Set Temperature: {set_temperature}°C, Set Humidity: {set_humidity}%")

            if temperature is not None and humidity is not None:
                # 온도와 습도 조건에 따른 제어
                # 온도가 낮을 때
                if temperature < set_temperature:
                    turn_on_lemp()
                elif temperature >= set_temperature:
                    turn_off_lemp()

                # 습도가 낮을 때
                if humidity < set_humidity:
                    turn_on_humidifier()
                elif humidity >= set_humidity:
                    turn_off_humidifier()

                # 온도와 습도 둘 다 높을 때
                if temperature >= set_temperature and humidity >= set_humidity:
                    pi.set_PWM_dutycycle(FAN_PIN, 255)  # 팬 최대 속도
                # 온도 또는 습도 하나만 높을 때
                elif temperature >= set_temperature or humidity <= set_humidity:
                    pi.set_PWM_dutycycle(FAN_PIN, 180)
                # 평상시
                else:
                    pi.set_PWM_dutycycle(FAN_PIN, 70)

            time.sleep(10)

        except RuntimeError as error:
            # 오류 처리
            print(f"RuntimeError: {error}")
            time.sleep(2)
        except Exception as error:
            # 기타 예외 처리
            print(f"Exception: {error}")
            time.sleep(2)

except KeyboardInterrupt:
    print("Program stopped")

finally:
    GPIO.cleanup()
    pi.stop()
