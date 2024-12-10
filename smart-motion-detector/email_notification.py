import smtplib
from config import EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_RECEIVER

def send_email(sensor_id):
    subject = "Motion Detected!"
    body = f"Motion was detected on Sensor {sensor_id}."
    message = f"Subject: {subject}\n\n{body}"
    
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, message)
        print(f"Email sent for Sensor {sensor_id}.")
    except Exception as e:
        print(f"Failed to send email: {e}")
