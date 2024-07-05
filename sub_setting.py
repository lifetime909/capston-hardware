import json
import paho.mqtt.client as mqtt

broker_address = '43.202.1.105'
topic = "cage/CAGE-X3J9-K4LQ-Z7WP2"

def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code.is_failure:
        print(f"Failed to connect: {reason_code}. loop_forever() will retry connection")
    else:
        print ("connect cage/CAGE-X3J9-K4LQ-Z7WP2")
        # we should always subscribe from on_connect callback to be sure
        # our subscribed is persisted across reconnections.
        client.subscribe(topic)

def on_message(client, userdata, msg):
    print("메시지 수신")
    try:
        # 메시지의 payload를 문자열로 디코드한 후 JSON으로 파싱
        new_data = json.loads(msg.payload.decode('utf-8'))  # json.load() 대신 json.loads() 사용

        # 'data.json' 파일이 존재하는지 확인하고, 존재한다면 파일의 내용을 읽어서 파이썬 객체로 변환
        try:
            with open('data.json', 'r') as file:
                data = json.load(file)  # 파일에서는 json.load() 사용
        except FileNotFoundError:
            # 파일이 존재하지 않는 경우, 새로운 데이터로 시작
            data = {}
        
        # 필요한 데이터 업데이트
        data.update(new_data)
        
        # 파일에 업데이트된 데이터 쓰기
        with open('data.json', 'w') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)  # 예쁘게 인코딩하기 위해 ensure_ascii와 indent 사용
        print("데이터 업데이트 완료")
    except Exception as e:
        print(f"Error: {e}")

mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_connect
mqttc.on_message = on_message

mqttc.connect(broker_address, 1883, 60)  # MQTT 브로커 주소와 포트

print ("connect broker")

# 네트워크 트래픽을 처리, 콜백 실행 등 루프 시작
try:
    mqttc.loop_forever()
except KeyboardInterrupt:
    print("프로그램이 사용자에 의해 중단되었습니다.")
    # 필요한 종료 처리 로직을 추가할 수 있습니다.
    mqttc.disconnect()
