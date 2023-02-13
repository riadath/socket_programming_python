import os
import struct
import socket
import threading
import random

IP = '10.33.2.97'
PORT = 4498
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"


dns_records = {}
file_in = open("dns_records.txt","r")
lines = file_in.readlines()
for record in lines:
    temp = record.split()
    dns_records[temp[0]] = []

for record in lines:
    temp = record.split()
    dns_records[temp[0]].append((temp[1],temp[2],temp[3]))


def handle_client(data, addr,server):
    print(f"[RECEIVED MESSAGE] {data} from {addr}.")
    print(data," <<recieved Data")
    
    response = struct.pack('hhl',5,5,4)
    server.sendto(response,addr)

    # record_list = []
    # try:
    #     record_list = dns_records[data]
    # except Exception as e:
    #     server.send("Incorrect Domain Name".encode(),addr)
    #     return
    
    # rnd_tuple = record_list[random.randrange(len(record_list)-1)]
    # server.send(f"{rnd_tuple[0]},{rnd_tuple[1]}".encode())

            
def main():
   
    print("[STARTING] Server is starting")
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind(ADDR)
    print(f"[LISTENING] Server is listening on {IP}:{PORT}.")

    while True:
        data, addr = server.recvfrom(SIZE)
        data = data.decode(FORMAT)
        print(f"[RECEIVED MESSAGE] {data} from {addr}.")
       
        thread = threading.Thread(target=handle_client, args=(data, addr,server))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

if __name__ == "__main__":
    main()