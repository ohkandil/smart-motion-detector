import blynklib
import RPi.GPIO as GPIO
import threading
import time
from sensors.ultrasonic_servo import set_servo_angle, initial_angle_1, initial_angle_2, servo_1, servo_2, GPIO_TRIGGER_1, GPIO_ECHO_1, GPIO_TRIGGER_2, GPIO_ECHO_2, distance

BLYNK_TEMPLATE_NAME = "Raspberry pi"

with open("/home/iot/Documents/blynk_key.txt", "r") as file:
    BLYNK_AUTH = file.readline().strip()
    BLYNK_TEMPLATE_ID = file.readline().strip()

blynk = blynklib.Blynk(BLYNK_AUTH)

# Flags to track manual control
manual_control_1 = False
manual_control_2 = False

# Virtual pins for Blynk buttons
VIRTUAL_PIN_SERVO_1 = 1
VIRTUAL_PIN_SERVO_2 = 2

def handle_ultrasonic_control():
    """Automatically control servo motors based on ultrasonic sensor readings."""
    while True:
        global manual_control_1, manual_control_2

        # Ultrasonic sensor 1 control
        if not manual_control_1:
            dist_1 = distance(GPIO_TRIGGER_1, GPIO_ECHO_1)
            if dist_1 <= 10:
                set_servo_angle(servo_1, 90)  # Rotate servo to 90 degrees
            else:
                set_servo_angle(servo_1, initial_angle_1)  # Return to initial angle

        # Ultrasonic sensor 2 control
        if not manual_control_2:
            dist_2 = distance(GPIO_TRIGGER_2, GPIO_ECHO_2)
            if dist_2 <= 10:
                set_servo_angle(servo_2, 90)  # Rotate servo to 90 degrees
            else:
                set_servo_angle(servo_2, initial_angle_2)  # Return to initial angle

        time.sleep(0.1)

# Blynk button handlers
@blynk.VIRTUAL_WRITE(VIRTUAL_PIN_SERVO_1)
def control_servo_1(value):
    """Manually control servo motor 1."""
    global manual_control_1
    if int(value[0]) == 1:
        manual_control_1 = True
        set_servo_angle(servo_1, 90)
        print("Manual control ON for Servo 1")
    else:
        manual_control_1 = False
        set_servo_angle(servo_1, initial_angle_1)
        print("Manual control OFF for Servo 1")

@blynk.VIRTUAL_WRITE(VIRTUAL_PIN_SERVO_2)
def control_servo_2(value):
    """Manually control servo motor 2."""
    global manual_control_2
    if int(value[0]) == 1:
        manual_control_2 = True
        set_servo_angle(servo_2, 90)
        print("Manual control ON for Servo 2")
    else:
        manual_control_2 = False
        set_servo_angle(servo_2, initial_angle_2)
        print("Manual control OFF for Servo 2")

def blynk_thread():
    """Run the Blynk event loop."""
    blynk.run()

# Main script execution
if __name__ == '__main__':
    try:
        # Initialize servos to their initial angles
        set_servo_angle(servo_1, initial_angle_1)
        set_servo_angle(servo_2, initial_angle_2)

        # Start the ultrasonic control thread
        threading.Thread(target=handle_ultrasonic_control, daemon=True).start()

        # Start the Blynk thread
        blynk_thread()

    except KeyboardInterrupt:
        print("Exiting program.")
        GPIO.cleanup()
