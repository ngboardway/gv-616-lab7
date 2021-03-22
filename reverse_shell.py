import socket
from threading import Thread
import subprocess
import atexit

HOST = 'localhost'
PORT = 5678

class CliThread(Thread):
    def __init__(self, address, port):
        Thread.__init__(self)
        self.address = address
        self.port = port 

    def run(self):
        while True:
            # Constantly receive data and decode.
            data = client_socket.recv(1024).decode()
            # If no data is present break the thread.
            if not data: break
            # If the data meets conditional close the program.
            if data.rstrip() == "CLOSE!":
                s.close()
                break
            # Execute command and retreive output
            output = subprocess.getoutput(data)
            # Send the output back to the client.
            client_socket.send(output.encode())
        client_socket.close()

# Create a socket on HOST listening on PORT
s = socket.socket()
# Allow reuse of address
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
threads = []

# Constantly listen for incoming connections.
while True:
    s.listen(1)
    (client_socket, (address, port)) = s.accept()
    # Spawn a new thread for each connection
    thread = CliThread(address, port)
    thread.start()
    threads.append(thread)

atexit.register(s.close())