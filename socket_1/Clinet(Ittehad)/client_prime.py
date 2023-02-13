# An example script to connect to Google using socket
# programming in Python
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
    host_ip = '10.33.2.97'
except socket.gaierror:
 
    # this means could not resolve the host
    print ("there was an error resolving the host")
    sys.exit()
 
# connecting to the server
s.connect((host_ip, port)) 
print ("the socket has successfully connected to Akib's server")

while True:

    #I send data
    number = input()
    s.send(number.encode())

    #I receive data
    print(s.recv(1024).decode())
