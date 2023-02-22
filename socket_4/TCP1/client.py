import random as rnd
import socket
clientSocket = socket.socket()

HOST = '127.0.0.1'
PORT = 869
BUFFER_SIZE = 4
HEADER_SIZE = 20
print('Waiting for connection response')
try:
    clientSocket.connect((HOST, PORT))
except socket.error as e:
    print(str(e))
res = clientSocket.recv(BUFFER_SIZE)


def create_header(
                src_port = 88,  #2 bytes
                dest_port = 88, #2 bytes
                seq = 0,   #4 bytes 
                ack = 0,   #4 bytes
                if_ack = 0, #ack = 1 -> if acknowledgement, 0 otherwise
                syn = 0, #syn = 1-> if synch req
                window_size = 0, #2 bytes
                checksum = 0, #2 bytes
                urgent_pointer = 0, #2 bytes
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
        int.from_bytes(header[13:13]),\
        int.from_bytes(header[14:14]),\
        int.from_bytes(header[15:16]),\



EST_STATE = False
CUR_SEQ = 0
CUR_ACK = 0
WINDOW_SIZE = 36

RECV_DATA = b''

def main():
    while True:
        #send/receive here
        if not EST_STATE:
            #connection establishment phase

            clientSocket.send(create_header(
                seq=CUR_SEQ,
                if_ack=0,
                syn=1,
                window_size = WINDOW_SIZE
            ))

            header = clientSocket.recv(HEADER_SIZE)
            seq,ack,if_ack,syn,window_size = retrieve_header(header)
            
            clientSocket.send(create_header(
                seq=CUR_SEQ + BUFFER_SIZE,
                ack=CUR_ACK,
                if_ack=1,
                syn = 0,
                window_size=WINDOW_SIZE
            ))   

            EST_STATE = True
        else: 
            #data transfer phase
            
            seq,ack,if_ack,syn,window_size = retrieve_header(clientSocket.recv(20))
            data  = clientSocket.recv(BUFFER_SIZE)

            print(data)
            if seq == CUR_SEQ:
                RECV_DATA += data
                CUR_SEQ = ack
                CUR_ACK = seq + BUFFER_SIZE
                WINDOW_SIZE -= BUFFER_SIZE 
            else:
                clientSocket.send(create_header(
                    seq=CUR_SEQ + BUFFER_SIZE,
                    ack=CUR_ACK,
                    if_ack=1,
                    syn = 0,
                    window_size=WINDOW_SIZE
                ))

if __name__ == "__main__":
    main()