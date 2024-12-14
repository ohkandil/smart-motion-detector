# import multiprocessing
# import subprocess
# import time
# from sensors.motion_sensors import arm_motion_sensor
# import RPi.GPIO as GPIO  

# def run_script(script_path):
#     subprocess.run(["python3", script_path])

# def main():
#     # Step 1: Arm the motion sensor
#     print("Arming the motion sensor...")
#     arm_motion_sensor()

#     # Step 2: Create separate processes for each script
#     scripts = [
#         "sensors/motion_sensors.py",
#         "notifications/email_notifier.py",
#         "integrations/adafruit_integration.py"
#     ]

#     processes = []

#     for script in scripts:
#         GPIO.cleanup()
#         process = multiprocessing.Process(target=run_script, args=(script,))
#         processes.append(process)
#         print(f"Starting script: {script}")
#         process.start()
#         time.sleep(1)  # 1-second delay between starting scripts

#     # Wait for all processes to complete
#     for process in processes:
#         process.join()

# if __name__ == "__main__":
#     main()


import multiprocessing
import subprocess
import time
from sensors.motion_sensors import arm_motion_sensor
import RPi.GPIO as GPIO

# Lock to synchronize GPIO access
gpio_lock = multiprocessing.Lock()

def run_script(script_path):
    subprocess.run(["python3", script_path])

def main():
    # Step 1: Arm the motion sensor
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
        process = multiprocessing.Process(target=run_script, args=(script,))
        processes.append(process)
        print(f"Starting script: {script}")
        process.start()
        time.sleep(1)  # 1-second delay between starting scripts

    # Wait for all processes to complete
    for process in processes:
        process.join()

    # Clean up GPIO resources after all processes have finished
    GPIO.cleanup()

if __name__ == "__main__":
    main()
