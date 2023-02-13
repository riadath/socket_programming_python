import socket # for socket
import sys
 
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print ("Socket successfully created")
except socket.error as err:
    print ("socket creation failed with error %s" %(err))
 
# default port for socket
port = 1234
 
try:
    host_ip = '127.0.0.1'
except socket.gaierror:
    # this means could not resolve the host
    print ("there was an error resolving the host")
    sys.exit()
 
# connecting to the server
s.connect((host_ip, port)) 
print ("the socket has successfully connected to Akib's server")

while True:

    print(s.recv(1024).decode())

    # send account name
    name = input()
    s.send(name.encode())

    print(s.recv(1024).decode())

    pin = input()
    s.send(pin.encode())

    print(s.recv(1024).decode())

    while True:

        cmd = input()
        s.send(cmd.encode())
        print(s.recv(1024).decode())

        if cmd == "deposit" or cmd == "withdraw":
            amount = input()
            s.send(amount.encode())
            print(s.recv(1024).decode())








