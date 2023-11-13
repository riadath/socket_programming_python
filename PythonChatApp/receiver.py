import random as rnd
import socket
import time


connection = socket.socket()
def setup_connection(HOST,PORT):
    print('Waiting for connection response')
    connection.connect((HOST, PORT))
    res = connection.recv(1024)
    print(res.decode())


def create_header(
        src_port=88,  #2 bytes
        dest_port=88,  #2 bytes
        seq=0,  #4 bytes 
        ack=0,  #4 bytes
        if_ack=0,  #ack = 1 -> if acknowledgement, 0 otherwise
        syn=0,  #syn = 1-> if synch req
        window_size=0,  #2 bytes
        checksum=0,  #2 bytes
        urgent_pointer=0,  #2 bytes
):
    return src_port.to_bytes(2) + \
           dest_port.to_bytes(2) + \
           seq.to_bytes(4) + \
           ack.to_bytes(4) + \
           if_ack.to_bytes(1) + \
           syn.to_bytes(1) + \
           window_size.to_bytes(2) + \
           checksum.to_bytes(2) + \
           urgent_pointer.to_bytes(2)


#will return a tuple - > (seq_number, ack_number, if_ack, syn, window_size)


def retrieve_header(header):
    return \
        int.from_bytes(header[4:8]),\
        int.from_bytes(header[8:12]),\
        int.from_bytes(header[12:13]),\
        int.from_bytes(header[13:14]),\
        int.from_bytes(header[14:16])


def time_ms():
    return int(time.perf_counter() * 1000)

def receive_data():
    HEADER_SIZE = 20
    CONST_rwnd = 100
    TIMEOUT = 500  #ms


    max_seg_size = 16
    recv_data = b''
    expected_seq = 0
    rwnd = CONST_rwnd


    len_file = int.from_bytes(connection.recv(HEADER_SIZE)[4:8])
    print(len_file, "bytes to be received")
    while True:
        #data transfer phase
        seq, ack, data = 0, 0, b''
        st_time = time_ms()
        while (time_ms() - st_time) < TIMEOUT:
            try:
                seq,ack,if_ack,syn,window_size = \
                retrieve_header(connection.recv(HEADER_SIZE))
                data = connection.recv(max_seg_size)
                recv_data += data

                # print("seq:", seq)

                rwnd -= max_seg_size
                expected_seq += max_seg_size

                if rwnd < max_seg_size:
                    break

            except Exception as e:
                continue

        if expected_seq + max_seg_size >= len_file:
            break

        if rwnd < max_seg_size:
            rwnd += rnd.randint(1, 4) * max_seg_size
            rwnd = min(rwnd, CONST_rwnd)

        #cummilitive acknowledgement
        connection.send(
            create_header(seq=ack,
                            ack=expected_seq + max_seg_size,
                            window_size=rwnd))
        
    return recv_data

def main():
    setup_connection('127.0.0.1',869)
    while(True):
        try:
            res = connection.recv(1024).decode()
            if res == 'yes':
                rec_data = receive_data()
                print('>>>>',rec_data)
        except:
            # print('hoy nai')
            continue
if __name__ == "__main__":
    main()