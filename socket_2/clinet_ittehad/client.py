import socket
ClientMultiSocket = socket.socket()
host = '10.33.2.97'
port = 2037
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

    response = ClientMultiSocket.recv(4096).decode()

    print( response )

    if response == "Incorrect File Name" : 
        continue

    #recieve data
    file = open(Input, 'wb')

# Keep receiving data from the server
    sz = int(ClientMultiSocket.recv(1024).decode())
    line = ClientMultiSocket.recv( min(4096,sz) )
    while(line):
        print(sz)
        print(line)
        file.write(line)
        sz = int(ClientMultiSocket.recv(1024))
        line = ClientMultiSocket.recv( min(4096,sz) )
        if not line:
            break
    file.close()
    print('File has been received successfully.')
ClientMultiSocket.close()   
