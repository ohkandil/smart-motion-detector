import zmq
import blynklib
import threading

BLYNK_TEMPLATE_NAME = "Motion Detection"

with open("/home/iot/Documents/blynk_key.txt", "r") as file:
    BLYNK_AUTH = file.readline().strip()
    BLYNK_TEMPLATE_ID = file.readline().strip()

blynk = blynklib.Blynk(BLYNK_AUTH)

def blynk_thread():
    """Runs the Blynk loop in a separate thread."""
    print("Starting Blynk service...")
    blynk.run()
    blynk.connect()

def send_ultrasonic_data_to_blynk(distance):
    """Send ultrasonic sensor data to Blynk."""
    blynk.virtual_write(1, distance)  # Assuming virtual pin V1 for ultrasonic data
    print(f"Sent ultrasonic data to Blynk: {distance}")

def motion_triggered():
    """Handles motion detected events."""
    print("Motion detected!")
    blynk.notify("Motion detected!")