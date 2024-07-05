import paho.mqtt.client as mqtt
import time
import board
import adafruit_dht
import json  # JSON 처리를 위한 모듈
import RPi.GPIO as GPIO
import pigpio

# GPIO 핀 번호 설정
HUM_PIN = 27
LEMP_PIN = 22
FAN_PIN = 18
DHT_PIN = board.D17

# GPIO 설정
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

# MQTT 브로커 설정
broker_address = '43.202.1.105'
broker_port = 1883

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))

mqttc = mqtt.Client()
mqttc.on_message = on_message

mqttc.connect(broker_address, broker_port, 60)
mqttc.loop_start()

print("connect mqtt")

# 가습기 모듈 On
def turn_on_humidifier():
    GPIO.output(HUM_PIN, GPIO.HIGH)  # 릴레이 켜기
    print("Humidifier turned on")

# 가습기 모듈 Off
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

            # 설정된 온도와 습도
            set_temperature = data["temperature"]
            set_humidity = data["humidity"]

            # DHT22 센서 데이터 측정
            temperature = dhtDevice.temperature
            humidity = dhtDevice.humidity

            print(f"Measured Temperature: {temperature}°C, Humidity: {humidity}%")
            print(f"Set Temperature: {set_temperature}°C, Set Humidity: {set_humidity}%")

            if temperature is not None and humidity is not None:
                # 센서 데이터를 JSON 형식으로 변환
                sensor_data = {
                    "serialCode": "CAGE-X3J9-K4LQ-Z7WP2",
                    "temperature": temperature,
                    "humidity": humidity
                }
                json_data = json.dumps(sensor_data)  # Python 객체를 JSON 문자열로 변환

                # MQTT 브로커로 JSON 데이터 발행
                mqttc.publish("sensor/data", json_data)
                print(f"Published: {json_data}")

                # 온도와 습도 조건에 따른 제어
                if temperature < set_temperature:
                    turn_on_lemp()
                else:
                    turn_off_lemp()

                if humidity < set_humidity:
                    turn_on_humidifier()
                else:
                    turn_off_humidifier()

                if temperature >= set_temperature and humidity >= set_humidity:
                    pi.set_PWM_dutycycle(FAN_PIN, 255)  # 팬 최대 속도
                elif temperature >= set_temperature or humidity <= set_humidity:
                    pi.set_PWM_dutycycle(FAN_PIN, 180)
                else:
                    pi.set_PWM_dutycycle(FAN_PIN, 70)

            time.sleep(10)  # 1분 간격으로 데이터 측정 및 전송

        except RuntimeError as error:
            print(f"RuntimeError: {error}")
            time.sleep(2)
        except Exception as error:
            print(f"Exception: {error}")
            time.sleep(2)

except KeyboardInterrupt:
    print("Program stopped")

finally:
    GPIO.cleanup()
    pi.stop()
    mqttc.disconnect()
    mqttc.loop_stop()
