import random as rnd
import socket
import time

clientSocket = socket.socket()

HOST = '127.0.0.1'
PORT = 869

print('Waiting for connection response')
try:
    clientSocket.connect((HOST, PORT))
except socket.error as e:
    print(str(e))
res = clientSocket.recv(1024)
print(res.decode())

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
        int.from_bytes(header[12:13]),\
        int.from_bytes(header[13:14]),\
        int.from_bytes(header[14:16])


BUFFER_SIZE = 200
HEADER_SIZE = 20



def main():
    len_file = 6090 #this is to terminate after file tranfer
    file_end = 0    # ideally it would be done through the 
                    # FIN flag in the header
    CONST_WINDOW_SIZE = 1000
    EST_STATE = False

    CUR_SEQ = 9000

    WINDOW_SIZE = CONST_WINDOW_SIZE

    EXPECTED_SEQ = 0
    TIMEOUT = 500 #ms
    RECV_DATA = b''

    file_in = open("__INPUT.txt","wb")

    # clientSocket.settimeout(1)
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
            EXPECTED_SEQ = seq
            print("EST STATE : ",
            "SEQ:",seq,"ACK_NO:",ack,"ACK:",
            if_ack,"SYN:",syn,"WINDOW SIZE:",window_size)
            
            clientSocket.send(create_header(
                seq=CUR_SEQ + BUFFER_SIZE,
                ack=0,
                if_ack=1,
                syn = 0,
                window_size=WINDOW_SIZE
            ))   

            EST_STATE = True
        else: 
            #data transfer phase
            # print("CUR DATA:",CUR_SEQ,CUR_ACK,WINDOW_SIZE)
            clientSocket.send(create_header(
                seq=EXPECTED_SEQ,
                ack=EXPECTED_SEQ + BUFFER_SIZE,
                window_size=WINDOW_SIZE
            ))
            st_time = int(time.perf_counter() * 1000)
            seq,ack,data = 0,0,b''
    
            while (int((time.perf_counter() - st_time)*1000) - st_time) < TIMEOUT:
                try:
                    seq,ack,if_ack,syn,window_size = \
                    retrieve_header(clientSocket.recv(HEADER_SIZE))
                    data=clientSocket.recv(BUFFER_SIZE)
                    # RECV_DATA += data
                    file_in.write(data)
                    file_end += BUFFER_SIZE
                    # print(data)
                    WINDOW_SIZE -= BUFFER_SIZE
                    EXPECTED_SEQ += BUFFER_SIZE

                    if WINDOW_SIZE < BUFFER_SIZE:
                        break
                except Exception as e:
                    e = str(e)
                    print(e)

            #randomly emptying the buuffer buffer -> application
            if WINDOW_SIZE < BUFFER_SIZE:
                WINDOW_SIZE += rnd.randint(1,36) * BUFFER_SIZE
                WINDOW_SIZE = min(WINDOW_SIZE,CONST_WINDOW_SIZE)


            #cummilitive acknowledgement
            clientSocket.send(create_header(
                seq=ack,
                ack=EXPECTED_SEQ + BUFFER_SIZE,
                window_size=WINDOW_SIZE
            ))

            if file_end >= len_file:
                clientSocket.close()
                file_in.close()
                # print(RECV_DATA)

                break
    print("DATA RECIEVED")
            
            

if __name__ == "__main__":
    main()