from blynkapi import Blynk
import time

# Define your Blynk authentication token
BLYNK_AUTH_TOKEN = '8YWOIEcxtxr_tKs_bcX5HJ8Ibz-y-gXJ'

# Set up Blynk instance
blynk = Blynk(BLYNK_AUTH_TOKEN)

# Virtual pins for ultrasonic data (for sensor readings)
VIRTUAL_PIN_SENSOR_1 = 1  # Virtual pin for sensor 1 distance data
VIRTUAL_PIN_SENSOR_2 = 2  # Virtual pin for sensor 2 distance data

# Digital pin assignments for Blynk (used to represent LED status)
BLYNK_LED_PIN_1 = 1  # Digital pin for LED 1 (automatically switches between 1 and 0)
BLYNK_LED_PIN_2 = 2  # Digital pin for LED 2 (automatically switches between 1 and 0)

# Function to send ultrasonic data and control LEDs automatically via Blynk
def send_ultrasonic_data_to_blynk(dist_1, dist_2):
    try:
        # Sending ultrasonic data to Blynk Virtual Pins
        blynk.virtual_write(VIRTUAL_PIN_SENSOR_1, dist_1)  # Write to virtual pin for sensor 1
        blynk.virtual_write(VIRTUAL_PIN_SENSOR_2, dist_2)  # Write to virtual pin for sensor 2
        print(f"Sent ultrasonic data to Blynk - Sensor 1: {dist_1} cm, Sensor 2: {dist_2} cm")

        # Automatically update LED status based on distance
        led_1_status = 1 if dist_1 <= 10 else 0  # LED 1 on if distance <= 10 cm
        led_2_status = 1 if dist_2 <= 10 else 0  # LED 2 on if distance <= 10 cm

        # Send LED status to Blynk digital pins (1 = ON, 0 = OFF)
        blynk.digital_write(BLYNK_LED_PIN_1, led_1_status)  # LED 1 control
        blynk.digital_write(BLYNK_LED_PIN_2, led_2_status)  # LED 2 control
        print(f"Sent LED status to Blynk - LED 1: {led_1_status}, LED 2: {led_2_status}")
    except Exception as e:
        print(f"Error sending data to Blynk: {e}")

# Blynk thread to handle Blynk communication
def blynk_thread():
    while True:
        try:
            blynk.run()  # Keep Blynk connection alive and process events
            time.sleep(0.1)
        except KeyboardInterrupt:
            break
