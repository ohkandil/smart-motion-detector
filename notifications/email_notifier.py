import smtplib
from email.mime.text import MIMEText
import zmq
from datetime import datetime, timedelta
import os

# Email Configuration
with open('/home/iot/Documents/email_cred.txt', 'r') as file:
    EMAIL = file.readline().strip()
    PASSWORD = file.readline().strip()

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
last_event_time = None

print(f"Process ID: {os.getpid()}")
# process id

# Function to send an email when motion is detected
def send_email_notification(sensor_id, distance):
    global last_event_time

    current_time = datetime.now()
    if last_event_time and (current_time - last_event_time) < timedelta(minutes=1):
        print("Duplicate event detected within a minute, skipping email.")
        return

    last_event_time = current_time

    msg = MIMEText(f"Motion detected on sensor {sensor_id} at {current_time.strftime('%Y-%m-%d %H:%M:%S')}. Distance: {distance:.1f} cm")
    msg['Subject'] = "Motion Alert"
    msg['From'] = EMAIL
    msg['To'] = EMAIL

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL, PASSWORD)
        server.send_message(msg)

    print(f"Email sent: Motion detected on sensor {sensor_id} at {current_time.strftime('%Y-%m-%d %H:%M:%S')}. Distance: {distance:.1f} cm")

# Subscribe to ZeroMQ events and handle notifications
def notify_via_email():
    # Initialize ZeroMQ subscriber
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect("tcp://localhost:5555")  # Connect to the motion detector's publisher
    socket.subscribe("")  # Subscribe to all messages

    print("Email notifier running...")

    while True:
        event = socket.recv_json()  # Receive a motion event

        print(f"Received event: {event}")
        send_email_notification(sensor_id=event['sensor'], distance=event['distance'])

if __name__ == "__main__":
    notify_via_email()  # Start listening for motion events