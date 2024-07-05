import socket
import requests
import json

def get_ip_address():
    # 소켓을 사용하여 실제 네트워크 인터페이스의 IP 주소를 가져옵니다.
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # 연결이 없는 상태에서 IP 주소를 얻기 위해 소켓을 사용합니다.
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
    except Exception as e:
        print(f"Failed to get IP address: {e}")
        ip_address = "127.0.0.1"
    finally:
        s.close()
    return ip_address

def send_ip_to_server(serial_code, location1):
    url = "http://54.180.158.4:8000/api/set-location"
    data = {
        "serialCode": serial_code,
        "location": location
    }
    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.post(url, data=json.dumps(data), headers=headers)
        if response.status_code == 200:
            print("IP address sent successfully.")
        else:
            print(f"Failed to send IP address. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    ip_address = get_ip_address()
    serial_code = "CAGE-X3J9-K4LQ-Z7WP2"  # 실제 시리얼 코드로 변경
    location = ip_address  # IP 주소를 location으로 사용
    send_ip_to_server(serial_code, location)
