import zmq
from gpiozero import LED, MotionSensor
from time import sleep
from history_logging.log_creation import setup_logger, log_motion_event

# Create objects to refer to the LED and the PIR sensor
# pir = MotionSensor(17, pull_up=False)  # Use pull-down resistor for the PIR sensor

# Control variables
motion_sensor_status = False

# Setup logger
log_file = 'motion_events.log'
logger = setup_logger(log_file)

# Arm or disarm the PIR sensor
def arm_motion_sensor():
    global motion_sensor_status

    if motion_sensor_status:
        motion_sensor_status = False
        log_motion_event(logger, "Motion Sensor OFF")
        print("Motion Sensor OFF")
    else:
        motion_sensor_status = True
        log_motion_event(logger, "Motion Sensor ON")
        print("Motion Sensor ON")

# Main function to monitor motion and publish events via ZeroMQ
def motion_detector():
    global motion_sensor_status

    # Initialize ZeroMQ publisher
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:5555")  # Publish events on port 5555

    log_motion_event(logger, "Motion detector running...")
    print("Motion detector running...")

    while True:
        pir = MotionSensor(17, pull_up=False)
        if motion_sensor_status and pir.motion_detected:
            socket.send_json({"sensor": 17, "state": "motion_detected"})
            log_motion_event(logger, "Motion detected! Publishing event...")
            print("Motion detected! Publishing event...")
            sleep(1)  # Delay to avoid flooding the message queue
        else:
            sleep(0.1)  # Check again quickly
        pir.close()

if __name__ == "__main__":
    arm_motion_sensor()  # Arm the sensor when the script starts
    motion_detector()    # Start detecting motion