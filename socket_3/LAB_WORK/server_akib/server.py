import socket
import os
import random
from _thread import *

ServerSideSocket = socket.socket()

host = '10.33.2.97'
port = 2030
ThreadCount = 0

try:
    ServerSideSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Socket is listening..')
ServerSideSocket.listen(5)

dns_records = {}
file_in = open("dns_records.txt","r")
lines = file_in.readlines()
for record in lines:
    temp = record.split()
    dns_records[temp[0]] = []

for record in lines:
    temp = record.split()
    dns_records[temp[0]].append((temp[1],temp[2],temp[3]))

print(dns_records)

def server_thread(connection):
    connection.send('Server Is Working'.encode())
    while True:
        #send/receive here
        data = connection.recv(2048).decode()
        print(data," <<recieved Data")
        record_list = []
        try:
            record_list = dns_records[data]
        except Exception as e:
            connection.send("Incorrect Domain Name".encode())
            continue
        
        rnd_tuple = record_list[random.randrange(len(record_list)-1)]
        connection.send(f"{rnd_tuple[0]},{rnd_tuple[1]}".encode())
        if not data:
            break
        
    connection.close()


while True:
    Client, address = ServerSideSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    
    try:
        start_new_thread(server_thread, (Client, ))
    except Exception as e:
        print(e)
    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount))
