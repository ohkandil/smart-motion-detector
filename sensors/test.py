from gpiozero import MotionSensor
import zmq
from time import sleep

def log_sensor_reading(sensor_pin, state):
    print(f"Sensor {sensor_pin}: {state}")

def monitor_sensors():
    # Initialize sensors
    sensors = [MotionSensor(pin) for pin in [14, 15, 18]]
    
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:5555")  # Publish sensor states

    print("Monitoring motion sensors...")
    while True:
        for sensor in sensors:
            sleep(0.5)
            print(sensor.pin, ": ",sensor.motion_detected)
            if sensor.motion_detected:  # Wait for motion on the current sensor
                # log_sensor_reading(sensor.pin, "motion_detected")
                
                # Send a message when motion is detected
                # socket.send_json({"sensor": sensor.pin, "state": "motion_detected"})
                log_sensor_reading(sensor.pin, "motion_detected")
                print({"sensor": sensor.pin, "state": "motion_detected"})

monitor_sensors()