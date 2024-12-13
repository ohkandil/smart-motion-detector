from gpiozero import MotionSensor
from signal import pause

# Initialize the motion sensor (connect it to GPIO pin 4)
pir = MotionSensor(14)

# Define actions for motion detection
def motion_detected():
    print("Motion detected!")

def motion_stopped():
    print("Motion stopped!")

# Link the sensor to the action functions
pir.when_motion = motion_detected
pir.when_no_motion = motion_stopped

# Keep the script running
print("Motion sensor is active. Waiting for motion...")
pause()
