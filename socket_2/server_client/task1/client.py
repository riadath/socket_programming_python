import socket
import random

ClientMultiSocket = socket.socket()
host = '127.0.0.1'
port = 8080
print('Waiting for connection response')
try:
    ClientMultiSocket.connect((host, port))
except socket.error as e:
    print(str(e))
res = ClientMultiSocket.recv(4096)
ClientMultiSocket.settimeout(1)
while True:
    #send data
    Input = input('File Name: ')

    ClientMultiSocket.send(Input.encode())

    response = ClientMultiSocket.recv(1024).decode()

    print( response )

    if response == "Incorrect File Name" : 
        continue

    #recieve data
    file = open(f"{random.randint(1,10000)}rec"+Input, 'wb')

# Keep receiving data from the server
    line = ClientMultiSocket.recv(1024)
    while(line):
        file.write(line)
        try:
            line = ClientMultiSocket.recv(1024)
        except:
            break
        if not line or line == b'':
            file.close()
            break
    file.close()
    print('File has been received successfully.')
ClientMultiSocket.close()   
