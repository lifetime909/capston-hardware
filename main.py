import subprocess
import threading
import time

def run_ip_setting():
    subprocess.run(["python3", "set_ip.py"])

#def run_sensor_publisher():
#    subprocess.run(["python3", "pub_DHT_json.py"])

def run_sensor_subscriber():
    subprocess.run(["python3", "sub_setting.py"])

def run_controller():
#    subprocess.run(["python3", "total_controll.py"])
    subprocess.run(["python3", "total_test.py"])

def run_stream():
    subprocess.run(["python3", "camera_stream.py"])

if __name__ == "__main__":
    ip_thread = threading.Thread(target=run_ip_setting)
#    pub_sensor_thread = threading.Thread(target=run_sensor_publisher)
    sub_sensor_thread = threading.Thread(target=run_sensor_subscriber)
    controll_thread = threading.Thread(target=run_controller)
    stream_thread = threading.Thread(target=run_stream)

    ip_thread.start()
    time.sleep(5) # IP 설정 후 다른 스레드 시작

#    pub_sensor_thread.start()
    sub_sensor_thread.start()
    controll_thread.start()
    stream_thread.start()

    ip_thread.join()
#   pub_sensor_thread.join()
    sub_sensor_thread.join()
    controll_tread.join()
    stream_tread.join()
