import socket
import time
from _thread import *
from enum import Enum


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
                rwnd = 0, #2 bytes
                checksum = 0, #2 bytes
                urgent_pointer = 0, #2 bytes
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

def time_ms():
    return int(time.perf_counter() * 1000)

#test file data
file_data = b'In view, a humble vaudevillian veteran, cast vicariously as \
both victim and villain by the vicissitudes of Fate. This visage'

# file_data = open("sample.txt","rb")

# print(len(file_data))

FILE_END = len(file_data)
MSS = 4
HEADER_SIZE = 20



print("FILE END : ",FILE_END)

def server_thread(connection):
    connection.send('Server Is Connected'.encode())
    # connection.settimeout(1)

    #start
    class STATE(Enum):
        EST_STATE = 0
        SLOW_START = 1
        CONGESTION_AVOIDANCE = 2
        FAST_RECOVERY = 3


    conn_state = STATE.EST_STATE
    file_pointer = 0
    cur_seq = 0
    cur_ack = 0
    prev_ack = 0
    st_time = time_ms()

    #for congestion control
    cwnd = MSS    
    timeout = 50 #ms
    ssthresh = 0
    dupACKcount = 0
    rwnd = 0
    available_window = MSS;
    
    while True:
        #send/receive here
        if conn_state == STATE.EST_STATE:
            #connection establishment phase

            header = connection.recv(HEADER_SIZE)
            seq,ack,if_ack,syn,rwnd = retrieve_header(header)
            ssthresh = rwnd

            #DEBUG______
            print("EST STATE : ",
            "SEQ:",seq,"ACK_NO:",ack,"ACK:",
            if_ack,"SYN:",syn,"WINDOW SIZE:",rwnd)
            #DEBUG______

            if syn == 0:
                cur_seq = ack
                conn_state = STATE.SLOW_START
            else:
                connection.send(create_header(
                    seq = cur_seq,
                    ack = seq + MSS,
                    if_ack = 1,
                    syn = 1
                ))
        else:
            #data tranfer phase
            available_window = min(cwnd,rwnd)
            while available_window >= MSS:
                connection.sendall(create_header(
                    seq=cur_seq,
                ) + file_data[cur_seq:(cur_seq+MSS)])
                
                available_window -= MSS
                cur_seq += MSS
                st_time = time_ms()

            cur_ack = cur_seq
            seq,ack,if_ack,syn,rwnd = retrieve_header(connection.recv(HEADER_SIZE))
            
            #duplicate ack
            print("ACK:",ack,"rwnd:",rwnd)
            print("============\n",conn_state.name,"\n============")

            # if ack == prev_ack:
            #     dupACKcount += 1
            # else:
            #     dupACKcount = 0
            # if ack == cur_ack:
            #     cwnd += MSS
            #     if cwnd >= ssthresh:
            #         cwnd += MSS * MSS // cwnd
            # if dupACKcount >= 3:
            #     print("---------------------------------------->",
            #     "3 DUPLICATE ACKS FOUND")
            #     dupACKcount = 0
            #     ssthresh = cwnd // 2
            #     cwnd = MSS
            #     cur_seq = prev_ack
            
            # if (time_ms() - st_time) > timeout:
            #     print("TIMEOUT !!! ")
            #     ssthresh = cwnd // 2
            #     cwnd = MSS
            #     cur_ack = ack
            #     st_time = time_ms()


            if conn_state == STATE.SLOW_START:
                #new ack
                if cur_ack == ack:
                    dupACKcount = 0
                    cwnd += MSS
                    if cwnd >= ssthresh:
                        conn_state = STATE.CONGESTION_AVOIDANCE
                        continue
                if dupACKcount == 3:
                    print("3 Duplicate ACK found !!!!!!")
                    ssthresh = cwnd//2
                    dupACKcount = 0
                    cwnd = ssthresh + 3*MSS
                    cur_seq = prev_ack
                    conn_state = STATE.FAST_RECOVERY

                #duplicate ack
                if ack == prev_ack:
                    dupACKcount += 1
                else:
                    dupACKcount = 0
                
                #timeout
                prev_ack = ack
                if (time_ms() - st_time) > timeout:
                    print("Timeout!!!!")
                    ssthresh = cwnd // 2
                    cwnd = MSS
                    dupACKcount = 0
                    st_time = time_ms()

            elif conn_state == STATE.CONGESTION_AVOIDANCE:
                #new ack
                if cur_ack == ack:
                    dupACKcount = 0
                    cwnd += int(MSS * (MSS/cwnd))
                if dupACKcount == 3:
                    print("3 Duplicate ACK found !!!!!!")
                    ssthresh = cwnd//2
                    dupACKcount = 0
                    cwnd = ssthresh + 3*MSS
                    cur_seq = prev_ack
                    conn_state = STATE.FAST_RECOVERY
                #duplicate ack
                if ack == prev_ack:
                    dupACKcount += 1
                else:
                    dupACKcount = 0
                #timeout
                prev_ack = ack
                if (time_ms() - st_time) > timeout:
                    print("Timeout!!!!")
                    ssthresh = cwnd // 2
                    cwnd = MSS
                    dupACKcount = 0
                    st_time = time_ms()
                    conn_state = STATE.SLOW_START

            elif conn_state == STATE.FAST_RECOVERY:

                #new ack
                if cur_ack == ack:
                    dupACKcount = 0
                    cwnd = ssthresh
                    conn_state = STATE.CONGESTION_AVOIDANCE
                
                #duplicate ack
                if ack == prev_ack:
                    cur_seq = prev_ack
                    cwnd += MSS   
                #timeout
                prev_ack = ack
                if (time_ms() - st_time) > timeout:
                    print("Timeout!!!!")
                    ssthresh = cwnd // 2
                    cwnd = MSS
                    dupACKcount = 0
                    st_time = time_ms()
                    conn_state = STATE.SLOW_START
            
            # prev_ack = ack
            print("------------------>cwnd:",cwnd,"ssthresh:",ssthresh)
            if cur_seq >= FILE_END:
                break


    # connection.close()
    print("DATA SENT")



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