import paho.mqtt.client as mqtt
import time
import board
import adafruit_dht

pin = board.D4
dhtDevice = adafruit_dht.DHT11(pin)

broker_address = '54.180.158.4'
broker_port = 1883
mqtt_username = "ras" # 사용자 이름을 여기에 입력하세요
mqtt_password = "0000" # 비밀번호를 여기에 입력하세요


mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

mqttc.connect(broker_address, broker_port, 60)
# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.

# 사용자 이름과 비밀번호 설정
mqttc.username_pw_set(mqtt_username, mqtt_password)

mqttc.loop_start()
print ("connect mqtt")
# Our application produce some messages
msg_info = mqttc.publish("test/raspi", "my message", qos=1)

while True:
    try:
        temperature = dhtDevice.temperature
        humidity = dhtDevice.humidity

        mqttc.publish("test/raspi", f"온도: {temperature}, 습도: {humidity}")
        time.sleep(2)
    except RuntimeError as error:
        print(error.args[0])

mqttc.disconnect()
mqttc.loop_stop()
