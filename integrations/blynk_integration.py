from BlynkLib import Blynk
import threading

BLYNK_TEMPLATE_ID = "TMPL2SeEV2-DB"
BLYNK_TEMPLATE_NAME = "Motion Detection"

BLYNK_AUTH = "D0axc7KXGn_2-QqsszyJBEf9QjkvCYQi"
blynk = Blynk(BLYNK_AUTH)


def blynk_thread():
    """Runs the Blynk loop in a separate thread."""
    print("Starting Blynk service...")
    blynk.run()

def motion_triggered():
    """
    Handles motion detected events.
    Sends a notification and updates the Blynk dashboard.
    """
    print("Motion detected! Sending notification to Blynk...")
    blynk.virtual_write(1, "Motion detected!")
    blynk.notify("Motion detected in your monitored area!")

@blynk.on("V0")  # Virtual pin 0 handler
def v0_write_handler(value):
    """Handles writes to virtual pin V0."""
    print(f"Data received on V0: {value}")

def start_blynk():
    """Starts the Blynk loop in a background thread."""
    threading.Thread(target=blynk_thread, daemon=True).start()