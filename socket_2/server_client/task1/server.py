import socket
import os
from _thread import *

ServerSideSocket = socket.socket()

host = '172.19.31.121'
port = 8080
ThreadCount = 0

try:
    ServerSideSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Socket is listening..')
ServerSideSocket.listen(5)


def multi_threaded_client(connection):
    connection.send('Server Is Working'.encode())
    while True:
        #send/receive here
        data = "";
        try:
            data = connection.recv(1024)
            print('File Name:',data.decode());
        except OSError as e:
            continue
        try:
            file = open(data.decode(),"rb")
            connection.send('Sending File'.encode())
        except FileNotFoundError as e:
            connection.send('Incorrect File Name'.encode())
            continue

        line = file.read(1024)
        while(line):
            connection.send(line)
            line = file.read(1024)
            print(line)
            if not line or line == b'':
                break
        file.close()

        if not data:
            break
        
        connection.close()



while True:
    Client, address = ServerSideSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    
    try:
        start_new_thread(multi_threaded_client, (Client, ))
    except Exception as e:
        continue
    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount))
ServerSideSocket.close()