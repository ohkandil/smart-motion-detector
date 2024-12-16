import zmq
from gpiozero import MotionSensor, LED
from time import sleep

  # Use GPIO 17 for the PIR sensor

motion_sensor_status = False
# toggles
def arm_motion_sensor():
    global motion_sensor_status

    if motion_sensor_status:
        motion_sensor_status = False
        print("Motion Sensor OFF")
    else:   
        motion_sensor_status = True
        print("Motion Sensor ON")

def motion_detector():
    global motion_sensor_status

    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:5555")  # Publish events on port 5555

    print("Motion detector running...")

    while True:
        if motion_sensor_status:
            if pir.motion_detected:
                socket.send_json({"sensor": 17, "state": "motion_detected"})
                print("Motion detected! Publishing event...")
                led.on()
                sleep(1)
                led.off()
                sleep(2.5)
            else:
                print("No motion detected")
                sleep(0.1)  # Check again quickly

if __name__ == "__main__":
    pir = MotionSensor(17)
    led = LED(23)
    arm_motion_sensor()  # Arm the sensor when the script starts
    motion_detector()    # Start detecting motion