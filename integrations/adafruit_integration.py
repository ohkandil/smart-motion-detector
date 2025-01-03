import zmq
from Adafruit_IO import Client, RequestError
import time

# Adafruit IO Configuration
with open("/home/iot/Documents/adafruitio_key.txt", "r") as file:
    ADAFRUIT_IO_KEY = file.readline().strip()
    ADAFRUIT_IO_USERNAME = file.readline().strip() 

aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

# Define feed names for sensors
SENSOR_FEEDS = {
    18: "iot-ultrasonic-feed-1",  # Feed for the first ultrasonic sensor
    22: "iot-ultrasonic-feed-2"   # Feed for the second ultrasonic sensor
}

# Ensure all feeds exist on Adafruit IO
def initialize_feeds():
    print("Initializing Adafruit IO feeds...")
    for sensor_id, feed_name in SENSOR_FEEDS.items():
        for attempt in range(3):  # Retry up to 3 times
            try:
                # Check if the feed exists, if not, create it
                aio.feeds(feed_name)
                print(f"Feed {feed_name} is ready.")
                break
            except RequestError as e:
                print(f"Error initializing feed {feed_name}: {e}")
                if attempt < 2:
                    print("Retrying...")
                    time.sleep(5)  # Wait for 5 seconds before retrying
                else:
                    print("Failed to initialize feed after 3 attempts. Skipping.")
                    break

# Function to send sensor data to Adafruit IO
def send_to_adafruit(sensor_id, state):
    feed_name = SENSOR_FEEDS.get(sensor_id)
    if not feed_name:
        print(f"Unknown sensor ID {sensor_id}. Skipping Adafruit IO update.")
        return
    aio.send(feed_name, state)
    print(f"Sent data to {feed_name}: {state}")

# Function to send ultrasonic sensor data to Adafruit IO
def send_ultrasonic_data(sensor_id, distance):
    feed_name = SENSOR_FEEDS.get(sensor_id)
    if not feed_name:
        print(f"Unknown sensor ID {sensor_id}. Skipping Adafruit IO update.")
        return
    aio.send(feed_name, distance)
    print(f"Sent ultrasonic data to {feed_name}: {distance}")