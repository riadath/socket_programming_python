import socket
from _thread import *
try:
    serverSocket = socket.socket()
except Exception as e:
    print(f"Failed to create socket. => {str(e)}")

server_addr = ('127.0.0.1',1969)
serverSocket.bind(server_addr)
serverSocket.listen(5)
print(f"Server is listening. binded to {server_addr}")

def handle_client(connection):
    while True:
        file_name = connection.recv(1024)

        try:
            fin = open(file_name.decode(),"rb")
            connection.send("File Found".encode())
        except:
            connection.send("Invalid File Name".encode())
            continue
        line = fin.read(1024)
        while line:
            connection.send(line)
            line = fin.read(1024)
            if line == b'':
                break
        fin.close()
        print("File Sent Successfully")
        
        if not file_name:
            break
    connection.close()


def main():
    thread_count = 1
    while True:
        connection,client_addr = serverSocket.accept()
        print(f"Connected to {client_addr[0]}:{client_addr[1]}")
        
        try:
            start_new_thread(handle_client,(connection,))
        except Exception as e:
            print(f"Could not start new therad => {str(e)}")

        print(f"Starting Thread : {thread_count}")
        thread_count += 1

    serverSocket.close()

if __name__ == "__main__":
    main()