import json
import paho.mqtt.client as mqtt
import struct

# MQTT 브로커 주소 및 구독할 토픽 설정
broker_address = '43.202.1.105'
topic = "cage/CAGE-X3J9-K4LQ-Z7WP2"

# MQTT 클라이언트가 브로커에 연결되었을 때 호출되는 콜백 함수
def on_connect(client, userdata, flags, reason_code, properties=None):
    if reason_code != 0:
        print(f"Failed to connect: {reason_code}")
    else:
        print("Connected to MQTT broker")
        # 브로커에 연결된 후 토픽을 구독
        client.subscribe(topic)

# MQTT 클라이언트가 메시지를 수신했을 때 호출되는 콜백 함수
def on_message(client, userdata, msg):
    print("Message received")
    try:
        # 메시지의 payload를 UTF-8로 디코딩
        payload = msg.payload.decode('utf-8')
        print(f"Payload: {payload}")
        # 디코딩된 payload를 JSON 객체로 변환
        new_data = json.loads(payload)

        # 'data.json' 파일을 읽어 기존 데이터를 로드하거나 파일이 없으면 빈 객체 생성
        try:
            with open('data.json', 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            data = {}

        # 새로운 데이터를 기존 데이터에 업데이트
        data.update(new_data)

        # 업데이트된 데이터를 'data.json' 파일에 저장
        with open('data.json', 'w') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        print("Data updated successfully")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
    except Exception as e:
        print(f"Error: {e}")

# MQTT 클라이언트가 구독 요청에 대한 응답을 받을 때 호출되는 콜백 함수
def on_subscribe(client, userdata, mid, granted_qos):
    print(f"Subscribed: {mid}, QoS: {granted_qos}")

# MQTT 클라이언트의 로깅 콜백 함수
def on_log(client, userdata, level, buf):
    print(f"Log: {buf}")

# MQTT 클라이언트 객체 생성 및 콜백 함수 설정
mqttc = mqtt.Client()
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.on_subscribe = on_subscribe
mqttc.on_log = on_log

# MQTT 브로커에 연결 시도
try:
    mqttc.connect(broker_address, 1883, 60)
    print("Connecting to broker...")
    mqttc.loop_start()
except Exception as e:
    print(f"Failed to connect to MQTT broker: {e}")

# MQTT 클라이언트의 메시지 루프를 시작
try:
    mqttc.loop_forever()
except KeyboardInterrupt:
    print("Program interrupted by user.")
    mqttc.disconnect()
    mqttc.loop_stop()
except struct.error as e:
    print(f"Struct error: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
