import socket
ClientMultiSocket = socket.socket()
host = '172.19.31.121'
port = 8080
print('Waiting for connection response')
try:
    ClientMultiSocket.connect((host, port))
except socket.error as e:
    print(str(e))
res = ClientMultiSocket.recv(4096)
while True:
    #send data
    Input = input('File Name: ')

    ClientMultiSocket.send(Input.encode())

    response = ClientMultiSocket.recv(1024).decode()

    print( response )

    if response == "Incorrect File Name" : 
        continue

    #recieve data
    file = open("rec"+Input, 'wb')

# Keep receiving data from the server
    line = ClientMultiSocket.recv(1024)
    while(line):
        file.write(line)
        line = ClientMultiSocket.recv(1024)
        if not line or line == b'':
            file.close()
            break
    file.close()
    print('File has been received successfully.')
ClientMultiSocket.close()   
