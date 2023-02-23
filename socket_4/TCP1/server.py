import socket
import os
from _thread import *



HOST = '127.0.0.1'
PORT = 869
ServerSideSocket = socket.socket()



#connection establishment
#____________________________
try:
    ServerSideSocket.bind((HOST, PORT))
except socket.error as e:
    print(e)


print('Socket is listening..')
ServerSideSocket.listen(5)
#____________________________




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




#test file data
file_data = b'In view, a humble vaudevillian veteran, cast vicariously as \
both victim and villain by the vicissitudes of Fate. This visage, \
no mere veneer of vanity, is a vestige of the vox populi, now vacant, vanished'


BUFFER_SIZE = 200
HEADER_SIZE = 20

file_data = open("sample.txt","rb")


def server_thread(connection):
    
    EST_STATE = False
    CUR_SEQ = 0
    CUR_ACK = 0
    RECV_WINDOW_SIZE = 0
    FILE_END_POINTER = 0
    connection.send('Server Is Connected'.encode())
    while True:
        #send/receive here
        # print("CUR DATA:",CUR_SEQ,CUR_ACK,RECV_WINDOW_SIZE)
        if not EST_STATE:
            #connection establishment phase

            header = connection.recv(HEADER_SIZE)
            seq,ack,if_ack,syn,window_size = retrieve_header(header)

            print("EST STATE : ",
            "SEQ:",seq,"ACK_NO:",ack,"ACK:",
            if_ack,"SYN:",syn,"WINDOW SIZE:",window_size)

            if syn == 0:
                CUR_SEQ = ack
                CUR_ACK = seq
                RECV_WINDOW_SIZE = window_size
                EST_STATE = True
            else:
                connection.send(create_header(
                    seq = CUR_SEQ,
                    ack = seq + 1,
                    if_ack = 1,
                    syn = 1
                ))

            
        else:
            #data tranfer phase
            send_data = file_data.read(BUFFER_SIZE)

            connection.sendall(create_header(
                seq= CUR_SEQ ,
                ack=CUR_ACK + BUFFER_SIZE,
                if_ack=0
             ) + send_data)
            
            seq,ack,if_ack,syn,window_size = retrieve_header(connection.recv(20))

            # print("FROM RECEIVER\n___________________________\n")
            # print("SEQ:",seq,"ACK_NO:",ack,"ACK:",
            # if_ack,"SYN:",syn,"WINDOW SIZE:",window_size)
            
            CUR_SEQ = ack 
            CUR_ACK = seq + BUFFER_SIZE
            RECV_WINDOW_SIZE = window_size

    connection.close()


#threading for multi client
#____________________________
def main():
    ThreadCount = 0 
    while True:
        Client, address = ServerSideSocket.accept()
        print('Connected to: ' + address[0] + ':' + str(address[1]))
        
        try:
            start_new_thread(server_thread, (Client, ))
        except Exception as e:
            continue
        ThreadCount += 1
        print('Thread Number: ' + str(ThreadCount))
    ServerSideSocket.close()

if __name__ == "__main__":
    main()

#____________________________