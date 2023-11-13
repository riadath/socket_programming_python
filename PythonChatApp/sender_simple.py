import socket
import os
from _thread import *



#connection establishment
#____________________________
HOST = '127.0.0.1'
PORT = 869
ServerSideSocket = socket.socket()
def setup_connection():
    try:
        ServerSideSocket.bind((HOST, PORT))
    except socket.error as e:
        print(e)

    print('Socket is listening..')
    ServerSideSocket.listen(5)
#____________________________



def send_data(connection,file_data):
    #simple socket loop to send data
    connection.settimeout(1)
    while True:
        try:
            connection.send(file_data)
            break
        except:
            continue
#receive data function
def receive_data(connection):
    #simple socket loop to receive data
    connection.settimeout(1)
    while True:
        try:
            data = connection.recv(1024)
            return data
        except:
            continue
#receive thread here
def recv_thread(connection):
    while True:
        try:
            res = connection.recv(1024).decode()
            if res == '230jkl3k93k34':
                rec_data = receive_data(connection)
                print('RECEIVER:',rec_data.decode())
        except:
            continue

def main():
    setup_connection()
    connection, address = ServerSideSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    connection.send('Server Is Connected'.encode())
    print("connection established")
    
    #receive thread
    start_new_thread(recv_thread,(connection,))
    while(True):
        to_send = input()
        connection.send(b'230jkl3k93k34');
        try:
            send_data(connection,to_send.encode())
        except:
            pass

if __name__ == "__main__":
    main()
