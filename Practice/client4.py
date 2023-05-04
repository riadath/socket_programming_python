import socket
import random
#create socket
try:
    clientSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
except Exception as e:
    print(f"Failed to create socket. => {str(e)}")

HOST = '127.0.0.1'
PORT = 1969



def main():
    try:
        clientSocket.connect((HOST,PORT))
    except Exception as e:
        print(f"Could not connect to : {(HOST,PORT)}")
        return
    
    print("Connected to server : ",(HOST, PORT))
    clientSocket.settimeout(1)

    #data transfer from here
    data = clientSocket.recv(1024)
    print(data.decode())

    clientSocket.sendall("hello from client".encode())
        
    clientSocket.close()

        

if __name__ == "__main__":
    main()