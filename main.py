import multiprocessing
import subprocess
import time
from sensors.ultrasonic_servo import distance
from integrations.blynk_integration import blynk_thread
from integrations.adafruit_integration import initialize_feeds, send_ultrasonic_data
from integrations.blynk_integration import send_ultrasonic_data_to_blynk
import threading

def run_script(script_path):
    subprocess.run(["python3", script_path])

def main():
    print("Initializing Adafruit IO feeds...")
    initialize_feeds()

    print("Starting Blynk service...")
    threading.Thread(target=blynk_thread).start()

    try:
        while True:
            dist = distance()
            print(f"Measured Distance = {dist:.1f} cm")
            send_ultrasonic_data(dist)  # Send data to Adafruit IO
            send_ultrasonic_data_to_blynk(dist)  # Send data to Blynk
            time.sleep(1)
    except KeyboardInterrupt:
        print("Measurement stopped by User")

if __name__ == "__main__":
    main()