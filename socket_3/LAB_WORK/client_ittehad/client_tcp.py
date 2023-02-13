import socket
ClientMultiSocket = socket.socket()
host = '10.33.2.97'
port = 2030
print('Waiting for connection response')
try:
    ClientMultiSocket.connect((host, port))
except socket.error as e:
    print(str(e))
res = ClientMultiSocket.recv(1024)
while True:
    #send data
    Input = input('File Name: ')

    while True:

        ClientMultiSocket.send(Input.encode())

        response = ClientMultiSocket.recv(1024).decode()

        type = response.split(",")[1]
        first = response.split(",")[0]

        print(first)
        print(type)

        if type == "A":
            print("IP address of the host is:")
            print(first)
            break
        else:
            ClientMultiSocket.send(first.encode())


# Keep receiving data from the server
ClientMultiSocket.close()
   