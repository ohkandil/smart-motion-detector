import threading
import time
from sensors.ultrasonic_servo import distance, set_servo_angle, GPIO_TRIGGER_1, GPIO_ECHO_1, GPIO_SERVO_1, GPIO_LED_1, GPIO_TRIGGER_2, GPIO_ECHO_2, GPIO_SERVO_2, GPIO_LED_2, initial_angle_1, initial_angle_2
from integrations.adafruit_integration import initialize_feeds, send_ultrasonic_data
from integrations.blynk_integration import blynk_thread, send_ultrasonic_data_to_blynk
import RPi.GPIO as GPIO

def main():
    print("Initializing Adafruit IO feeds...")
    initialize_feeds()

    print("Starting Blynk service...")
    threading.Thread(target=blynk_thread).start()

    try:
        # Initialize servos to their initial angles
        set_servo_angle(GPIO_SERVO_1, initial_angle_1)
        set_servo_angle(GPIO_SERVO_2, initial_angle_2)
        time.sleep(1)  # Allow time for servos to stabilize

        while True:
            dist_1 = distance(GPIO_TRIGGER_1, GPIO_ECHO_1)
            if dist_1 <= 10:
                print(f"Object detected within 10 cm by Sensor 1. Measured Distance = {dist_1:.1f} cm")
                set_servo_angle(GPIO_SERVO_1, 90)  # Rotate servo to 90 degrees
                GPIO.output(GPIO_LED_1, GPIO.HIGH)  # Turn on LED 1
            else:
                set_servo_angle(GPIO_SERVO_1, initial_angle_1)  # Rotate servo back to initial angle
                GPIO.output(GPIO_LED_1, GPIO.LOW)  # Turn off LED 1

            dist_2 = distance(GPIO_TRIGGER_2, GPIO_ECHO_2)
            if dist_2 <= 10:
                print(f"Object detected within 10 cm by Sensor 2. Measured Distance = {dist_2:.1f} cm")
                set_servo_angle(GPIO_SERVO_2, 90)  # Rotate servo to 90 degrees
                GPIO.output(GPIO_LED_2, GPIO.HIGH)  # Turn on LED 2
            else:
                set_servo_angle(GPIO_SERVO_2, initial_angle_2)  # Rotate servo back to initial angle
                GPIO.output(GPIO_LED_2, GPIO.LOW)  # Turn off LED 2

            # Send data to Adafruit IO and Blynk
            send_ultrasonic_data(dist_1)
            send_ultrasonic_data_to_blynk(dist_1)
            send_ultrasonic_data(dist_2)
            send_ultrasonic_data_to_blynk(dist_2)

            time.sleep(0.1)  # Reduce the sleep time to improve responsiveness

    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()

if __name__ == "__main__":
    main()