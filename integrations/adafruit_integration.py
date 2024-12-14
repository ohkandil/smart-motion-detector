import zmq
from Adafruit_IO import Client, RequestError

# Adafruit IO Configuration
ADAFRUIT_IO_KEY = "aio_IYwQ97XllAcuVvA8otJMBH7ghfnL"  # Replace with your Adafruit IO key
ADAFRUIT_IO_USERNAME = "Sherifhameed30"  # Replace with your Adafruit IO username
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

# Define feed names for motion sensors
SENSOR_FEEDS = {
    17: "iot-motion-feed"
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


# Function to send motion data to Adafruit IO
def send_to_adafruit(sensor_id, state):
    feed_name = SENSOR_FEEDS.get(sensor_id)
    if not feed_name:
        print(f"Unknown sensor ID {sensor_id}. Skipping Adafruit IO update.")
        return

    # Send state to Adafruit IO feed
    try:
        aio.send(feed_name, state)
        print(f"Sent data to Adafruit IO: {feed_name} -> {state}")
    except Exception as e:
        print(f"Failed to send data to Adafruit IO for {feed_name}: {e}")


# Subscribe to ZeroMQ events and forward to Adafruit IO
def adafruit_integration():
    # Initialize Adafruit IO feeds
    initialize_feeds()

    # Initialize ZeroMQ subscriber
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect("tcp://localhost:5555")  # Connect to the motion detector's publisher
    socket.subscribe("")  # Subscribe to all messages

    print("Adafruit integration running...")
    while True:
        event = socket.recv_json()  # Receive a motion event
        print(f"Received event: {event}")

        # Forward the event data to Adafruit IO
        sensor_id = event.get('sensor')
        state = event.get('state')
        if state == "motion_detected":
            send_to_adafruit(sensor_id, "motion_detected")
        
        elif state == "no_motion":
            send_to_adafruit(sensor_id, "no_motion")
        exit()
       


if __name__ == "__main__":
    adafruit_integration()  # Start the Adafruit integration
