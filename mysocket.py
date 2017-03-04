import socket
import sys
global sock
HOST, PORT = "localhost", 17429
HOST, PORT = "codebb.cloudapp.net", 17429
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))