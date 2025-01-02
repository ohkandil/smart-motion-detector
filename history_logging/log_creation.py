import csv
from datetime import datetime
from gpiozero import LED, MotionSensor
from time import sleep

# Motion sensor setup
led_status = LED(15)
pir = MotionSensor(17, pull_up=False)

# CSV log file
LOG_FILE = "motion_data.csv"

# Log motion events
def log_motion_event(sensor_id, state):
    with open(LOG_FILE, mode='a') as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now(), sensor_id, state])
    print(f"Logged: {datetime.now()} - Sensor {sensor_id} - {state}")

# Detect motion and log it
def motion_detector():
    while True:
        if pir.motion_detected:
            log_motion_event(sensor_id=17, state="motion_detected")
        else:
            log_motion_event(sensor_id=17, state="no_motion")
        sleep(1)  # Check every second

if __name__ == "__main__":
    print("Motion detector running...")
    motion_detector()
