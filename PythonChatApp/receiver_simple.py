import random as rnd
import socket
import time
from _thread import *


connection = socket.socket()
def setup_connection(HOST,PORT):
    print('Waiting for connection response')
    connection.connect((HOST, PORT))
    res = connection.recv(1024)
    print(res.decode())


def time_ms():
    return int(time.perf_counter() * 1000)

def receive_data():
    connection.settimeout(0.05)
    recv_data = b''
    #simple socket loop to receive data
    while True:
        try:
            data = connection.recv(1024)
            recv_data += data
        except:
            break
    
    return recv_data

#send_data fucntion
def send_data(file_data):
    #simple socket loop to send data
    connection.settimeout(0.05)
    while True:
        try:
            connection.send(file_data)
            break
        except:
            continue

def recv_thread():
    while True:
        try:
            res = connection.recv(1024).decode()
            if res == '230jkl3k93k34':
                rec_data = receive_data()
                print("RECEIVER: ",rec_data.decode())
                
        except:
            continue

def main():
    #start receiver thread
    HOST = '127.0.0.1'
    PORT = 869
    setup_connection(HOST,PORT)
    start_new_thread(recv_thread,())
    #send data from main thread
    while True:
        to_send = input()
        connection.send(b'230jkl3k93k34');
        try:
            send_data(to_send.encode())
        except:
            pass
if __name__ == "__main__":
    main()