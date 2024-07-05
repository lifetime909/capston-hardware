import pigpio
import time

FAN_PIN = 18  # GPIO18

pi = pigpio.pi()

if not pi.connected:
    exit()

# PWM 주파수를 25 kHz로 설정 (대부분의 팬에 표준)
pi.set_PWM_frequency(FAN_PIN, 25000)

try:
    while True:
        # 팬 속도 증가
        for duty_cycle in range(0, 256, 5):
            pi.set_PWM_dutycycle(FAN_PIN, duty_cycle)
            time.sleep(0.1)
        
        # 팬 속도 감소
        for duty_cycle in range(255, -1, -5):
            pi.set_PWM_dutycycle(FAN_PIN, duty_cycle)
            time.sleep(0.1)

except KeyboardInterrupt:
    pass

pi.set_PWM_dutycycle(FAN_PIN, 70)  # 팬을 끔
pi.stop()
