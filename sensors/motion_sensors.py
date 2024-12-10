from gpiozero import MotionSensor
import zmq

def monitor_sensors():
    sensors = [MotionSensor(pin) for pin in [17, 27, 22, 5, 6]]
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:5555")  # Publish sensor states

    print("Monitoring motion sensors...")
    while True:
        for i, sensor in enumerate(sensors):
            if sensor.motion_detected:
                socket.send_json({"sensor": i, "state": "motion_detected"})
