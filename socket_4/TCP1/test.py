import random as rnd
import socket
import time
import sys

#
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
    

def main():
    msg = create_header(seq=1, if_ack=1, checksum=1)
    print(msg)

if __name__ ==  "__main__":
    main()