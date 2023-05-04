import socket
import os
from _thread import *
import time
import random as rnd

connection = socket.socket()


def setup_connection(HOST, PORT):
    print('Waiting for connection response')
    connection.connect((HOST, PORT))
    res = connection.recv(1024)
    print(res.decode())


def time_ms():
    return int(time.perf_counter() * 1000)


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


#send_data fucntion
def send_data(connection, file_data):
    print(len(file_data), "bytes to be sent")
    #connection establishment
    FILE_END = len(file_data)
    HEADER_SIZE = 20

    max_seg_size = 8
    file_pointer = 0
    cur_seq = 0
    rwnd = 100
    connection.send(create_header(seq=len(file_data)))
    while True:
        # print("seq:", cur_seq, "rwnd:", rwnd)
        while rwnd >= max_seg_size:
            if cur_seq + max_seg_size >= FILE_END:
                to_send = file_data[cur_seq:FILE_END]
                connection.send(create_header(seq=cur_seq, ) + to_send)
                file_pointer += max_seg_size
                rwnd -= max_seg_size
                cur_seq += max_seg_size
                break
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
        print("ack:", ack, "rwnd:", rwnd)
    print("Data sent successfully")


def receive_data(connection):
    # print("Data receiving started")
    HEADER_SIZE = 20
    CONST_rwnd = 20

    connection.settimeout(1)

    max_seg_size = 8
    recv_data = b''
    expected_seq = 0
    rwnd = CONST_rwnd
    urgent_pointer = 0

    seq, ack, data = 0, 0, b''
    connection.send('230jkl3k93k34'.encode())
    while True:
        try:
            header = connection.recv(HEADER_SIZE)
            urgent_pointer = int.from_bytes(header[18:20])
            seq, ack, if_ack, syn, window_size = retrieve_header(header)

            data = connection.recv(max_seg_size)

            recv_data += data
            print("seq:", seq, "ack:", ack, "rwnd:", rwnd, "data:",
                  data.decode())

            rwnd -= max_seg_size
            expected_seq += max_seg_size

            if urgent_pointer == 1:
                print('rwmd increased', rwnd)
                rwnd += rnd.randint(5, 7) * max_seg_size
                rwnd = min(rwnd, CONST_rwnd)
                while urgent_pointer == 1:
                    try:
                        connection.send(
                            create_header(seq=ack,
                                        ack=expected_seq + max_seg_size,
                                        window_size=rwnd))
                        urgent_pointer = 0
                        break
                    except Exception as e:
                        print("Exception in sending ack")
                        pass
            elif urgent_pointer == 2:
                break

        except Exception as e:
            print("Exception in receiving data")
            continue

    print('End of data transfer')
    return recv_data


def recv_thread():
    while True:
        try:
            res = connection.recv(1024).decode()
            if res == '230jkl3k93k34':
                rec_data = receive_data(connection)
                print("RECEIVER: ", rec_data.decode())
        except:
            # print('hocce na')
            continue


def main():
    #start receiver thread
    HOST = '127.0.0.1'
    PORT = 869
    setup_connection(HOST, PORT)
    start_new_thread(recv_thread, ())
    #send data from main thread

    connection.settimeout(0.05)

    while True:
        to_send = input()
        connection.send(b'230jkl3k93k34')
        try:
            send_data(connection, to_send.encode())
        except:
            pass


if __name__ == "__main__":
    main()