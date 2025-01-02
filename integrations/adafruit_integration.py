import zmq
from Adafruit_IO import Client, RequestError

# Adafruit IO Configuration
with open("/home/iot/Documents/adafruitio_key.txt", "r") as file:
    ADAFRUIT_IO_KEY = file.readline().strip()
    ADAFRUIT_IO_USERNAME = file.readline().strip() 

aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

# Define feed names for sensors
SENSOR_FEEDS = {
    18: "iot-ultrasonic-feed"  # Feed for the ultrasonic sensor
}

# Ensure all feeds exist on Adafruit IO
def initialize_feeds():
    print("Initializing Adafruit IO feeds...")
    for sensor_id, feed_name in SENSOR_FEEDS.items():
        try:
            # Check if the feed exists, if not, create it
            aio.feeds(feed_name)
        except RequestError:
            aio.create_feed({'name': feed_name})
            print(f"Created feed: {feed_name}")
    print("All feeds are ready.")

# Function to send sensor data to Adafruit IO
def send_to_adafruit(sensor_id, state):
    feed_name = SENSOR_FEEDS.get(sensor_id)
    if not feed_name:
        print(f"Unknown sensor ID {sensor_id}. Skipping Adafruit IO update.")
        return
    aio.send(feed_name, state)
    print(f"Sent data to {feed_name}: {state}")

# Function to send ultrasonic sensor data to Adafruit IO
def send_ultrasonic_data(distance):
    feed_name = SENSOR_FEEDS.get(18)  # Assuming 18 is the ID for the ultrasonic sensor
    if not feed_name:
        print(f"Unknown sensor ID 18. Skipping Adafruit IO update.")
        return
    aio.send(feed_name, distance)
    print(f"Sent ultrasonic data to {feed_name}: {distance}")