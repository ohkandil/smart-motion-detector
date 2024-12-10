import logging

# Configure logging
logging.basicConfig(
    filename="motion_logs.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
)

def log_motion(sensor_id):
    logging.info(f"Motion detected on Sensor {sensor_id}")


# Use ai to analyze the logs
