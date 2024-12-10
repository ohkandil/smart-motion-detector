import zmq
import logging

logging.basicConfig(filename="motion_log.log", level=logging.INFO)

def log_events():
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect("tcp://localhost:5555")
    socket.subscribe("")  # Subscribe to all messages

    print("Logging events...")
    while True:
        event = socket.recv_json()
        logging.info(f"Sensor {event['sensor']} - {event['state']}")
