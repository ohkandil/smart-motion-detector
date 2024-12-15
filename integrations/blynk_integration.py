import zmq
from blynklib import Blynk
import threading


BLYNK_TEMPLATE_NAME = "Motion Detection"

with open("/home/iot/Documents/blynk_key.txt", "r") as file:
    BLYNK_AUTH = file.readline().strip()
    BLYNK_TEMPLATE_ID = file.readline().strip()

blynk = Blynk(BLYNK_AUTH)

def blynk_thread():
    """Runs the Blynk loop in a separate thread."""
    print("Starting Blynk service...")
    blynk.run()

def motion_triggered():
    """
    Handles motion detected events.
    Sends a notification and updates the Blynk dashboard.
    """
    print("Motion detected! Sending notification to Blynk...")
    blynk.virtual_write(1, "Motion detected!")
    blynk.notify("Motion detected in your monitored area!")

# Handle the virtual pin event manually
def v0_write_handler(pin, value):
    """Handles writes to virtual pin V0."""
    if pin == 'V0':
        print(f"Data received on V0: {value}")

# blynk.add_virtual_pin(0, write=v0_write_handler)

def start_blynk():
    """Starts the Blynk loop in a background thread."""
    threading.Thread(target=blynk_thread, daemon=True).start()

def blynk_integration():
    # Initialize ZeroMQ subscriber
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect("tcp://localhost:5555")  # Connect to the motion detector's publisher
    socket.subscribe("")  # Subscribe to all messages

    print("Blynk integration running...")
    start_blynk()

    while True:
        event = socket.recv_json()  # Receive a motion event
        print(f"Received event: {event}")

        # Trigger the motion event handler
        sensor_id = event.get('sensor')
        state = event.get('state')
        if state == "motion_detected":
            motion_triggered()

if __name__ == "__main__":
    blynk_integration()  # Start the Blynk integration