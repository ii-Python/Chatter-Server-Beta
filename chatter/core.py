# Modules
import socket
from .colors import colored

from .logging import verbose
from .config import load_config

from .client import ClientManager

# Initialization
__version__ = "1.0.32"
__author__ = "Benjamin O'Brien (iiPython)"

# Master class
class ChatterServer(object):

    def __init__(self, args):
        self.args = args
        self.config = {}

    def _generate_sock(self, host, port, config, max_connections = 5):

        verbose("Generating new socket...")

        # Create a new socket
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        server.bind((host, port))
        server.listen(max_connections)

        # Then create a client manager
        verbose("Creating client manager...")
        clients = ClientManager(config)

        verbose("Socket and client manager created.")

        return (server, clients)

    def load_config(self):

        """Loads configuration info from config.json"""

        # Load configuration
        verbose("Began loading configuration file.")
        
        try:

            self.config = load_config()

        except Exception as err:

            verbose("Failed while loading:", err)

            return {}

        print("Loaded configuration from config.json")

        print()
        server_name = input("Server name: ")

        self.config["server_name"] = server_name

        # Return our data
        return self.config

    def start(self):

        """Launches the Chatter server and begins an infinite response loop"""

        print(f"Chatter Server v{__version__}")
        
        config = self.load_config()

        print()
        print(f"Listening on {config['host']}:{config['port']}", f"with authentication code {config['code']}" if config["code"] else "")
        print()

        # Begin master loop
        server, internal = self._generate_sock(config["host"], config["port"], config)

        verbose("Server started, listening for requests!")
        while True:

            conn, addr = server.accept()

            verbose("Received connection from", addr)
            internal.add_client(addr, conn)
