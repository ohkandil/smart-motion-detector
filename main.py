import multiprocessing
import subprocess
import time
from history_logging.log_creation import setup_logger, log_motion_event
from sensors.motion_sensors import arm_motion_sensor

def run_script(script_path):
    subprocess.run(["python3", script_path])

def main():
    # Setup logger
    log_file = 'motion_events.log'
    logger = setup_logger(log_file)

    # Step 1: Arm the motion sensor
    log_motion_event(logger, "Arming the motion sensor...")
    print("Arming the motion sensor...")
    arm_motion_sensor()

    # Step 2: Create separate processes for each script
    scripts = [
        "sensors/motion_sensors.py",
        "notifications/email_notifier.py",
        "integrations/adafruit_integration.py"
    ]

    processes = []

    for script in scripts:
        # Reset GPIO pins before starting each script

        
        process = multiprocessing.Process(target=run_script, args=(script,))
        processes.append(process)
        log_motion_event(logger, f"Starting script: {script}")
        print(f"Starting script: {script}")
        process.start()
        time.sleep(1)  # 1-second delay between starting scripts

    # Wait for all processes to complete
    for process in processes:
        process.join()

if __name__ == "__main__":
    main()