import zmq

def send_someip():
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect("tcp://localhost:5555")
    socket.subscribe("")  # Subscribe to all sensor messages

    print("Sending SOME/IP messages...")
    while True:
        event = socket.recv_json()
        # Add SOME/IP logic here
        print(f"Simulating SOME/IP send: {event}")

if __name__ == "__main__":
    send_someip()