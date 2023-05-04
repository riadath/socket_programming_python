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
    while True:
        file_name = input("File Name/Path : ")
        clientSocket.send(file_name.encode())
        response = clientSocket.recv(1024).decode()
        if response == "Invalid File Name":
            continue
        fout = open(f"{random.randint(1,1000)}recv{file_name}","wb")
        
        line = clientSocket.recv(1024)
        while line:
            fout.write(line)
            try: 
                line = clientSocket.recv(1024)
            except TimeoutError as e:
                break
        
        fout.close()
        print("File Recieved Successfully")
        
    clientSocket.close()

        

if __name__ == "__main__":
    main()