
import multiprocessing
import subprocess
import time
import gpiozero as GPIO


def run_script(script_path):
    subprocess.run(["python3", script_path])

def main():
    # Step 1: Arm the motion sensor
    print("Arming the motion sensor...")
    # arm_motion_sensor()
    # motion_detector()


    # Step 2: Create separate processes for each script
    scripts = [
        "notifications/email_notifier.py",
        "integrations/adafruit_integration.py",
        "sensors/motion_sensors.py"
    ]

    processes = []

    for script in scripts:
        # Reset GPIO pins before starting each script
        # GPIO.cleanup()
        
        process = multiprocessing.Process(target=run_script, args=(script,))
        processes.append(process)
        print(f"Starting script: {script}")
        process.start()
        time.sleep(1)  # 1-second delay between starting scripts

    # Wait for all processes to complete
    for process in processes:
        process.join()

if __name__ == "__main__":
    main()