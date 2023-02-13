# An example script to connect to Google using socket
# programming in Python
import socket # for socket
import sys
 
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.1)
    print ("Socket successfully created")
except socket.error as err:
    print ("socket creation failed with error %s" %(err))
 
# default port for socket
port = 1235
id = 0
 
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
    id = int(pin)
    s.send(pin.encode())

    print(s.recv(1024).decode())

    while True:


        cmd = input()
        flag = True
        amount = 0
        if cmd == "deposit" or cmd == "withdraw":
            print("Enter amount:")
            amount = input()

        while flag:
            if cmd == "deposit" or cmd == "withdraw":
                # print(cmd)
                # print(amount)
                # print(id)
                s.send(f"{cmd} {amount} {id}".encode())
            else:
                s.send(f"{cmd} {id}".encode())
            try:
                flag = False
                print(s.recv(1024).decode())
                id += 1
            except socket.timeout as e:
                flag = True









