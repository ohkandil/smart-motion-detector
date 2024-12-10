# Assuming Adafruit IO setup
from Adafruit_IO import Client
import zmq

ADAFRUIT_KEY = "your_adafruit_key"
aio = Client(ADAFRUIT_KEY)

def push_to_adafruit():
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect("tcp://localhost:5555")
    socket.subscribe("")  # Subscribe to all sensor messages

    print("Pushing data to Adafruit IO...")
    while True:
        event = socket.recv_json()
        feed_name = f"sensor-{event['sensor']}"
        aio.send(feed_name, event['state'])
