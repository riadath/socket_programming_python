import socket

try:
    serverSocket = socket.socket()
except Exception as e:
    print(f"Failed to create socket. => {str(e)}")

server_addr = ('127.0.0.1',1969)
serverSocket.bind(server_addr)
serverSocket.listen(5)
print(f"Server is listening. binded to {server_addr}")




def main():
    connection,client_addr = serverSocket.accept()

    #data transfer from here
    connection.sendall("Hello from server".encode())
    data = connection.recv(1024)
    print(data.decode())

    serverSocket.close()

if __name__ == "__main__":
    main()