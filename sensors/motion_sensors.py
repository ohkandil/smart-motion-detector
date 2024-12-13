from gpiozero import MotionSensor
import zmq

def monitor_sensors():
    # sensors = [MotionSensor(pin) for pin in [14, 15, 18]]
    sensors = [14, 15, 18]
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:5555")  # Publish sensor states

    print("Monitoring motion sensors...")
    while True:
        # for i, sensor in enumerate(sensors):  # Create a copy of the list for iteration
        for i in sensors:
            pir = MotionSensor(i)
            pir.wait_for_motion()
            print(f"Motion detected on sensor pin {i}!")
            
            # if sensor.motion_detected:
            #     socket.send_json({"sensor": i, "state": "motion_detected"})
            #     print({"sensor": i, "state": "motion_detected"})


monitor_sensors()