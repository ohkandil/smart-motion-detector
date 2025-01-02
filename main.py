import threading
import time
import zmq
from sensors.ultrasonic_servo import distance, set_servo_angle, GPIO_TRIGGER_1, GPIO_ECHO_1, GPIO_SERVO_1, GPIO_LED_1, GPIO_TRIGGER_2, GPIO_ECHO_2, GPIO_SERVO_2, GPIO_LED_2, initial_angle_1, initial_angle_2, servo_1, servo_2
from integrations.adafruit_integration import initialize_feeds, send_ultrasonic_data
from integrations.blynk_integration import blynk_thread, send_ultrasonic_data_to_blynk
from notifications.email_notifier import notify_via_email
import subprocess
import RPi.GPIO as GPIO

def main():
    # Initialize ZeroMQ subscriber
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect("tcp://localhost:5555")
    socket.subscribe("")  # Subscribe to all messages
    
    initialize_feeds()
    threading.Thread(target=blynk_thread).start()

    print("Starting Email Notifier service...")
    threading.Thread(target=notify_via_email).start()

    # Initialize servos to their initial angles
    set_servo_angle(servo_1, initial_angle_1)
    set_servo_angle(servo_2, initial_angle_2)
    time.sleep(1)  # Allow time for servos to stabilize

    # Run ultrasonic_servo.py as a script

    subprocess.Popen(["python3", "sensors/ultrasonic_servo.py"])
        
    # try:
    #     while True:
    #         event = socket.recv_json()  # Receive data from ultrasonic sensors
    #         dist_1 = event["sensor_1"]
    #         dist_2 = event["sensor_2"]

    #         if dist_1 <= 10:
    #             print(f"Object detected within 10 cm by Sensor 1. Measured Distance = {dist_1:.1f} cm")
    #             set_servo_angle(servo_1, 90)  # Rotate servo to 90 degrees
    #             GPIO.output(GPIO_LED_1, GPIO.HIGH)  # Turn on LED 1
    #         else:
    #             set_servo_angle(servo_1, initial_angle_1)  # Rotate servo back to initial angle
    #             GPIO.output(GPIO_LED_1, GPIO.LOW)  # Turn off LED 1

    #         if dist_2 <= 10:
    #             print(f"Object detected within 10 cm by Sensor 2. Measured Distance = {dist_2:.1f} cm")
    #             set_servo_angle(servo_2, 90)  # Rotate servo to 90 degrees
    #             GPIO.output(GPIO_LED_2, GPIO.HIGH)  # Turn on LED 2
    #         else:
    #             set_servo_angle(servo_2, initial_angle_2)  # Rotate servo back to initial angle
    #             GPIO.output(GPIO_LED_2, GPIO.LOW)  # Turn off LED 2

    #         # Send data to Adafruit IO and Blynk
    #         send_ultrasonic_data(18, dist_1)
    #         send_ultrasonic_data_to_blynk(dist_1)
    #         send_ultrasonic_data(22, dist_2)
    #         send_ultrasonic_data_to_blynk(dist_2)

    #         time.sleep(0.1)  # Reduce the sleep time to improve responsiveness

    # except KeyboardInterrupt:
    #     print("Measurement stopped by User")
    #     GPIO.cleanup()

if __name__ == "__main__":
    main()