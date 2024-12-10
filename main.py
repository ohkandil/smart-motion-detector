import multiprocessing
from sensors.motion_sensors import monitor_sensors
from logging.logger import log_events
from integrations.adafruit_integration import push_to_adafruit
from integrations.someip_integration import send_someip
from notifications.email_notifier import notify_via_email

if __name__ == "__main__":
    processes = [
        multiprocessing.Process(target=monitor_sensors),
        multiprocessing.Process(target=log_events),
        multiprocessing.Process(target=push_to_adafruit),
        multiprocessing.Process(target=send_someip),
        multiprocessing.Process(target=notify_via_email)
    ]

    for process in processes:
        process.start()

    for process in processes:
        process.join()
