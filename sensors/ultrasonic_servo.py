import RPi.GPIO as GPIO
import time

# GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

# set GPIO Pins for the first ultrasonic sensor and servo motor
GPIO_TRIGGER_1 = 18
GPIO_ECHO_1 = 24
GPIO_SERVO_1 = 25
GPIO_LED_1 = 23

# set GPIO Pins for the second ultrasonic sensor and servo motor
GPIO_TRIGGER_2 = 22
GPIO_ECHO_2 = 27
GPIO_SERVO_2 = 17
GPIO_LED_2 = 4

# set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER_1, GPIO.OUT)
GPIO.setup(GPIO_ECHO_1, GPIO.IN)
GPIO.setup(GPIO_SERVO_1, GPIO.OUT)
GPIO.setup(GPIO_LED_1, GPIO.OUT)

GPIO.setup(GPIO_TRIGGER_2, GPIO.OUT)
GPIO.setup(GPIO_ECHO_2, GPIO.IN)
GPIO.setup(GPIO_SERVO_2, GPIO.OUT)
GPIO.setup(GPIO_LED_2, GPIO.OUT)

# Set up PWM for the servo motors
servo_1 = GPIO.PWM(GPIO_SERVO_1, 50)  # 50Hz frequency
servo_1.start(0)  # Initialization

servo_2 = GPIO.PWM(GPIO_SERVO_2, 50)  # 50Hz frequency
servo_2.start(0)  # Initialization

def distance(trigger, echo):
    # set Trigger to HIGH
    GPIO.output(trigger, True)

    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(trigger, False)

    StartTime = time.time()
    StopTime = time.time()

    # save StartTime
    while GPIO.input(echo) == 0:
        StartTime = time.time()

    # save time of arrival
    while GPIO.input(echo) == 1:
        StopTime = time.time()

    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2

    return distance

def set_servo_angle(servo, gpio_pin, angle):
    duty = angle / 18 + 2
    GPIO.output(gpio_pin, True)
    servo.ChangeDutyCycle(duty)
    time.sleep(0.5)
    GPIO.output(gpio_pin, False)
    servo.ChangeDutyCycle(0)

if __name__ == '__main__':
    try:
        # Initialize servos to 0 degrees
        set_servo_angle(servo_1, GPIO_SERVO_1, 0)
        set_servo_angle(servo_2, GPIO_SERVO_2, 0)
        time.sleep(1)  # Allow time for servos to stabilize

        while True:
            dist_1 = distance(GPIO_TRIGGER_1, GPIO_ECHO_1)
            if dist_1 <= 10:
                print(f"Object detected within 10 cm by Sensor 1, triggering servo motor 1. Measured Distance = {dist_1:.1f} cm")
                set_servo_angle(servo_1, GPIO_SERVO_1, 90)  # Rotate servo to 90 degrees
                GPIO.output(GPIO_LED_1, GPIO.HIGH)  # Turn on LED 1
            else:
                set_servo_angle(servo_1, GPIO_SERVO_1, 0)  # Rotate servo back to 0 degrees
                GPIO.output(GPIO_LED_1, GPIO.LOW)  # Turn off LED 1

            dist_2 = distance(GPIO_TRIGGER_2, GPIO_ECHO_2)
            if dist_2 <= 10:
                print(f"Object detected within 10 cm by Sensor 2, triggering servo motor 2. Measured Distance = {dist_2:.1f} cm")
                set_servo_angle(servo_2, GPIO_SERVO_2, 90)  # Rotate servo to 90 degrees
                GPIO.output(GPIO_LED_2, GPIO.HIGH)  # Turn on LED 2
            else:
                set_servo_angle(servo_2, GPIO_SERVO_2, 0)  # Rotate servo back to 0 degrees
                GPIO.output(GPIO_LED_2, GPIO.LOW)  # Turn off LED 2

            time.sleep(1)

    except KeyboardInterrupt:
        print("Measurement stopped by User")
        servo_1.stop()
        servo_2.stop()
        GPIO.cleanup()