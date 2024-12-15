#!/bin/bash
python3 ./sensors/motion_sensors.py &
python3 ./notifications/email_notifier.py &
python3 ./integrations/adafruit_integration.py &
exit 0