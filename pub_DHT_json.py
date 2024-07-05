import paho.mqtt.client as mqtt
import time
import board
import adafruit_dht
import json  # JSON 처리를 위한 모듈

pin = board.D17
dhtDevice = adafruit_dht.DHT22(pin)

broker_address = '43.202.1.105'
broker_port = 1883

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

mqttc.connect(broker_address, broker_port, 60)
mqttc.loop_start()

print("connect mqtt")

while True:
    try:
        temperature = dhtDevice.temperature
        humidity = dhtDevice.humidity

        if temperature is not None and humidity is not None:
            # 센서 데이터를 JSON 형식으로 변환
            data = {
		"serialCode": "CAGE-X3J9-K4LQ-Z7WP2",
                "temperature": temperature,
                "humidity": humidity
            }
            json_data = json.dumps(data)  # Python 객체를 JSON 문자열로 변환

            # MQTT 브로커로 JSON 데이터 발행
            mqttc.publish("sensor/data", json_data)
            print(f"Published: {json_data}")
        else:
            print("센서에서 데이터를 읽는 데 실패했습니다.")

        time.sleep(60)
    except RuntimeError as error:
        print(error.args[0])
        time.sleep(2)
    except Exception as e:
        print(f"Unexpected error: {e}")
        time.sleep(2)

mqttc.disconnect()
mqttc.loop_stop()
