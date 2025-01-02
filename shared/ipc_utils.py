import zmq

def get_publisher_socket(port):
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind(f"tcp://*:{port}")
    return socket

def get_subscriber_socket(port, topic=""):
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect(f"tcp://localhost:{port}")
    socket.subscribe(topic)
    return socket
