from gpiozero import LED, MotionSensor
from signal import pause

# Create objects to refer to the LED and the PIR sensor
led_status = LED(15)
pir = MotionSensor(17, pull_up=False)  # Use pull-down resistor for the PIR sensor

# Control variables
motion_sensor_status = False

# Arm or disarm the PIR sensor
def arm_motion_sensor():
    global motion_sensor_status

    if motion_sensor_status:
        motion_sensor_status = False
        led_status.off()
        print("Motion Sensor OFF")
    else:
        motion_sensor_status = True
        led_status.on()
        print("Motion Sensor ON")

# Detect motion and take action
def detect_motion():
    global motion_sensor_status

    if motion_sensor_status and pir.motion_detected:
        print("Motion Detected")
    else:
        print("No Motion")

# Assign a function to run when motion is detected
pir.when_motion = detect_motion

# Test the setup
arm_motion_sensor()
pause()
