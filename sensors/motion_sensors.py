import zmq
from gpiozero import LED, MotionSensor
from time import sleep

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


# Main function to monitor motion and publish events via ZeroMQ
def motion_detector():
    global motion_sensor_status

    # Initialize ZeroMQ publisher
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:5555")  # Publish events on port 5555

    print("Motion detector running...")

    while True:
        if motion_sensor_status and pir.motion_detected:
            print("Motion detected! Publishing event...")
            socket.send_json({"sensor": 17, "state": "motion_detected"})
            sleep(1)
            exit()  # Delay to avoid flooding the message queue
        else:
            sleep(0.1)  # Check again quickly


if __name__ == "__main__":
    arm_motion_sensor()  # Arm the sensor when the script starts
    motion_detector()    # Start detecting motion
