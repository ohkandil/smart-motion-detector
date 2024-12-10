from Adafruit_IO import Client
from config import ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY

aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

def send_to_adafruit(sensor_id):
    try:
        aio.send("motion_sensor", f"Motion detected on Sensor {sensor_id}")
        print(f"Data sent to Adafruit for Sensor {sensor_id}.")
    except Exception as e:
        print(f"Adafruit IO error: {e}")
