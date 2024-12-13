import smtplib
from email.mime.text import MIMEText
import zmq
# email notifier tested with dummy data and it works.
EMAIL = "iot450702@gmail.com"
PASSWORD = "xign cwhh wjho bzyi"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

def send_email_notification(event):
    msg = MIMEText(f"Motion detected on sensor {event['sensor']}")
    msg['Subject'] = "Motion Alert"
    msg['From'] = EMAIL
    msg['To'] = EMAIL

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL, PASSWORD)
        server.send_message(msg)

def notify_via_email():
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect("tcp://localhost:5555")
    socket.subscribe("")  # Subscribe to all sensor messages

    print("Email notifications enabled...")
    while True:
        event = socket.recv_json()
        # event = {
        #     'sensor': "testers"
        # }
        send_email_notification(event)

notify_via_email()