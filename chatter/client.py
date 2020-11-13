# Modules
import json
import socket

import threading
from .colors import colored

from .logging import verbose
from .commands import run_command

# Client class
class Client(object):

    def __init__(self, addr, conn, manager):
        self.addr = addr
        self.conn = conn
        self.manager = manager

    def is_admin(self):

        """Returns whether or not the user is an admin"""

        # If there arent any admins, everyone is an admin
        if not self.manager.config["admin_ips"]:

            return True

        # Check if ip is an admin
        ip, port = self.get_ip()

        return ip in self.manager.config["admin_ips"]

    def make_admin(self):

        # No need to do anything if they are already an admin
        if self.is_admin() and self.manager.config["admin_ips"]:

            return

        self.manager.config["admin_ips"].append(self.get_ip()[0])
        self.manager.save_config()

    def get_ip(self):

        """Returns the address that the client connected from"""

        return self.addr

    def disconnect(self):

        """Disconnects the client from the server."""

        verbose(f"{self.addr}: Received disconnect request, closing socket.")

        # Shutdown socket
        self.conn.shutdown(socket.SHUT_RDWR)
        self.conn.close()

        # Remove from internal database
        del self.manager.clients[self.addr]

        verbose(self.addr, "has disconnected successsfully.")

# Client manager class
class ClientManager(object):

    def __init__(self, config):
        self.clients = {}
        self.config = config

    def protocol(self, protocol, *args):

        proto = protocol.upper()

        for arg in args:

            proto += ":" + arg

        return proto.encode("UTF-8")

    def fetch_protocol(self, data):

        if ":" in data:

            name = data.split(":", 1)[0].lower()
            data = data.split(":", 1)[1]

            return (name, data)

        return (data.lower(), "")

    def save_config(self):

        open("config.json", "w").write(json.dumps(self.config, indent = 4))
        verbose("Configuration has been saved to config.json")

    def add_client(self, addr, conn):

        self.clients[addr] = Client(addr, conn, self)

        # Begin client loop
        thread = threading.Thread(target = self.loop_client, args = [addr])
        thread.start()

        verbose("Client loop started for", addr)

    def locate_user(self, name):

        # Loop through all of our clients
        for client in self.clients:

            try:

                # Check if the name matches
                if self.clients[client].name == name:

                    return self.clients[client]  # Return the client

            except:
                
                # This will raise an exception if the client hasn't sent a name request yet.
                # For now we silently ignore this since they aren't authenticated.
                pass

    def relay_message(self, message):

        # Loop through each client
        for client in self.clients:

            client = self.clients[client]

            # Make sure our client is logged in
            if client.authenticated:

                # Transmit our message
                client.conn.sendall(self.protocol("message-sent", message))

        # The server should also see whats happening
        print(message)

    def loop_client(self, addr):

        client = self.clients[addr]
        conn = client.conn

        # Perform some basic client-checking
        if addr[0] in self.config["banned_ips"]:

            verbose(addr[0], "is banned, disconnected!")

            # Client is banned
            conn.sendall(self.protocol("banned-ip"))
            return client.disconnect()

        elif self.config["code"]:

            verbose("Alerted", addr, "that this server requires authentication.")

            # Client needs to authentication
            conn.sendall(self.protocol("auth-required"))
            client.authenticated = False

        else:

            verbose(addr, "can proceed with the connection.")

            # Client can proceed with the connection
            conn.sendall(self.protocol("proceed"))
            client.authenticated = True

        # Handle client while its connected
        with conn:

            # Begin data loop
            while True:

                try: data = conn.recv(1024).decode("UTF-8")
                except: break  # Client disconnected

                # Fetch protocol from data
                proto, data = self.fetch_protocol(data)

                # Parse through our protocols
                if not client.authenticated:

                    # Client isn't authenticated yet
                    if proto == "authenticate":

                        verbose(addr, "is trying to authenticate...")

                        # Authenticate them
                        if data == str(self.config["code"]):

                            verbose(addr[0], "successfully authenticated, replied with auth-accepted.")

                            # Authentication successful
                            conn.sendall(self.protocol("auth-accepted"))
                            client.authenticated = True

                        else:

                            verbose(addr[0], "failed to authenticate, disconnected.")

                            # Authentication failed
                            conn.sendall(self.protocol("auth-rejected"))
                            return client.disconnect()

                # Client is authenticated and can make requests
                if proto == "request-name":
                    
                    # Send back the server name
                    verbose("Sent the server name to", addr)
                    conn.sendall(self.protocol("server-name", self.config["server_name"]))
                
                elif proto == "identify-user":

                    # Try to identify the user
                    if self.locate_user(data):

                        # Sorry, a user with that name already exists
                        verbose(addr[0], "tried to use an already existing username, disconnected.")

                        conn.sendall(self.protocol("user-exists"))
                        return client.disconnect()

                    # Proceed with connection
                    client.name = data
                    conn.sendall(self.protocol("proceed"))

                    verbose(addr, "can proceed with the connection.")

                    self.relay_message(colored(f"{client.name} has joined the server.", "green"))

                elif proto == "send-message":

                    # Make sure they have a name and transmit the message
                    try:

                        self.relay_message(f"[{client.name}]: {data}")

                        # Command handling
                        if data.startswith("/"):

                            run_command(self, client, data)
                            
                    except Exception as err:
                        
                        verbose("Silently ignoring error for", addr, ":", err)

                        # This will raise an exception if they don't have a name assigned yet
                        # If we catch this then people that aren't authenticated cannot send messages
                        pass

        # Remove client upon disconnect
        try: del self.clients[addr]
        except: pass
        
        self.relay_message(colored(f"{client.name} has disconnected from the server.", "red"))

        try: client.disconnect()
        except: pass  # It's alright if it fails to disconnect, since we likely will crash
