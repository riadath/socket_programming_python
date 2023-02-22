import socket
import os
from _thread import *

ServerSideSocket = socket.socket()

host = '10.33.2.97'
port = 2037
ThreadCount = 0
try:
    ServerSideSocket.bind((host, port))
except Exception as e:
    print(str(e))

print('Socket is listening..')
ServerSideSocket.listen(5)



def multi_threaded_client(connection):
    connection.send('Server Is Working'.encode())
    while True:
        #send/receive here
      
        data = connection.recv(1024)

        print('File Name:',data.decode());
        try:
            file = open(data.decode(),"rb")
            connection.send('Sending File'.encode())
        except FileNotFoundError as e:
            print('Wrong File Name')
            connection.send('Incorrect File Name'.encode())
        line = file.read(1024)
        connection.send(len(line).encode())
        while(line):
            connection.send(line)
            line = file.read(1024)
            print(line)
            if not line:
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
        print(e)
    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount))
ServerSideSocket.close()