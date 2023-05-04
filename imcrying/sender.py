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



def create_header(
        src_port=88,  #2 bytes
        dest_port=88,  #2 bytes
        seq=0,  #4 bytes 
        ack=0,  #4 bytes
        if_ack=0,  #ack = 1 -> if acknowledgement, 0 otherwise
        syn=0,  #syn = 1-> if synch req
        rwnd=0,  #2 bytes
        checksum=0,  #2 bytes
        urgent_pointer=0,  #2 bytes
):
    return src_port.to_bytes(2) + \
           dest_port.to_bytes(2) + \
           seq.to_bytes(4) + \
           ack.to_bytes(4) + \
           if_ack.to_bytes(1) + \
           syn.to_bytes(1) + \
           rwnd.to_bytes(2) + \
           checksum.to_bytes(2) + \
           urgent_pointer.to_bytes(2)

#will return a tuple - > (seq_number, ack_number, if_ack, syn, rwnd)
def retrieve_header(header):
    return \
        int.from_bytes(header[4:8]),\
        int.from_bytes(header[8:12]),\
        int.from_bytes(header[12:13]),\
        int.from_bytes(header[13:14]),\
        int.from_bytes(header[14:16])




def send_data_TCP(connection,file_data):
    print(len(file_data), "bytes to be sent")
    #connection establishment
    FILE_END = len(file_data)
    HEADER_SIZE = 20

    connection.settimeout(1)

    max_seg_size = 16
    file_pointer = 0
    cur_seq = 0
    rwnd = 100
    
    connection.send(create_header(seq=len(file_data)))
    while True:
        # print("seq:", cur_seq, "rwnd:", rwnd)
        while rwnd >= max_seg_size and cur_seq < FILE_END:
            try:
                to_send = file_data[cur_seq:(cur_seq + max_seg_size)]
                connection.send(create_header(seq=cur_seq, ) + to_send)
                file_pointer += max_seg_size
                rwnd -= max_seg_size
                cur_seq += max_seg_size

            except Exception as e:
                break

        if cur_seq >= FILE_END:
            break

        seq, ack, if_ack, syn, rwnd = retrieve_header(
            connection.recv(HEADER_SIZE))
        cur_seq = ack
        # print("ack:", ack, "rwnd:", rwnd)
    print("Data sent successfully")



def main():
    setup_connection()
    connection, address = ServerSideSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    connection.send('Server Is Connected'.encode())
    print("connection established")
    
    while(True):
        to_send = input("Enter Send String : ")
        connection.send(b'yes');
        try:
            send_data_TCP(connection,to_send.encode())
        except:
            print('hocce na')


if __name__ == "__main__":
    main()
