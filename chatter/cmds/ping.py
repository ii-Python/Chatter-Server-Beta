# Modules
import socket
from datetime import datetime

# Calculate ping time
def get_ping():

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Start timer
    start = datetime.now()

    # Try to connect
    try:

        s.connect(("74.125.26.102", 80))

        s.shutdown(socket.SHUT_RD)

    except socket.timeout:

        return 0

    except OSError:
        
        return 0

    # Stop timer
    runtime = (datetime.now() - start).total_seconds() * 1000

    return round(runtime)

# Command function
def ping(manager, author, args):

    """Standard ping command, returns server latency"""

    manager.relay_message(f"Pong! Server latency: {get_ping()}ms")
