import threading
from time import sleep
import zmq
# from sensors.ultrasonic_servo import  distance, set_servo_angle, GPIO_TRIGGER_1, GPIO_ECHO_1, GPIO_SERVO_1, GPIO_LED_1, GPIO_TRIGGER_2, GPIO_ECHO_2, GPIO_SERVO_2, GPIO_LED_2, initial_angle_1, initial_angle_2, servo_1, servo_2
# from integrations.adafruit_integration import initialize_feeds, send_ultrasonic_data
# from integrations.blynk_integration import blynk_thread, send_ultrasonic_data_to_blynk
# from notifications.email_notifier import notify_via_email
import subprocess
import RPi.GPIO as GPIO


y=(0.1)
subprocess.Popen(["python", 'sensors/ultrasonic_servo.py'])
sleep(y)
subprocess.Popen(["python", 'notifications/email_notifier.py'])
sleep (y)
subprocess.Popen(["python", 'integrations/blynk_tst.py'])
sleep (y)
subprocess.Popen(["python", 'integrations/adafruit_integration.py'])
sleep (y)

