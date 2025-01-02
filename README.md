Smart Motion Detection System
A modular IoT system designed for a university course project, built on a Raspberry Pi 3B+. The system uses multiple motion sensors to detect movement, logs the data, sends notifications, and integrates with third-party platforms like Adafruit IO and SOME/IP.

Features
Motion Detection: Tracks motion using five PIR sensors connected to the Raspberry Pi's GPIO pins.
Logging: Logs motion events to a local file for analysis and debugging.
Notifications: Sends email alerts when motion is detected.
Adafruit Integration: Pushes motion data to Adafruit IO for visualization and remote monitoring.
SOME/IP Integration: Sends motion events using the SOME/IP protocol for integration with automotive systems.
Modular Architecture: Each feature is implemented in a separate module for easy scalability and maintenance.

Hardware:

Raspberry Pi 3B+
5 PIR motion sensors (connected via GPIO pins)
Internet connection for Adafruit and email integration
Software:

Python 3.7+
Required Python libraries (see requirements.txt)

Setup
1. Clone the Repository
git clone https://github.com/ohkandil/smart_motion_detection.git
cd smart_motion_detection
2. Install Dependencies
It’s recommended to use a virtual environment:

python3 -m venv venv
source venv/bin/activate  # On Linux/Mac
venv\Scripts\activate     # On Windows

pip install -r requirements.txt
3. Configure Modules
Adafruit IO: Set your API key in adafruit_integration.py.
Email Notifications: Update email credentials in email_notifier.py.
4. Connect Hardware
Connect PIR sensors to GPIO pins on the Raspberry Pi. Ensure the pin numbers in motion_sensors.py match your setup.
Usage
1. Run the System
Start the main script to launch all components:

python main.py
2. Test Individual Components
To test specific modules, run their corresponding test scripts. For example:

python test_motion_sensors.py
python test_logger.py
How It Works
Motion Detection:
Each PIR sensor detects motion and sends a signal.
Inter-Process Communication (IPC):
Modules communicate using ZeroMQ to publish/subscribe to events.
Integrations:
Motion events are logged, pushed to Adafruit IO, sent via SOME/IP, and email alerts are triggered.
Contributing
Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

License
This project is licensed under the MIT License. See the LICENSE file for details.

Acknowledgments
University IoT Course Team
Adafruit for their excellent IoT tools
Raspberry Pi Foundation for providing an amazing platform
