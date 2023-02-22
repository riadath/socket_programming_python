
def create_header(
                src_port = 88,  #2 bytes
                dest_port = 88, #2 bytes
                seq = 0,   #4 bytes 
                ack = 0,   #4 bytes
                if_ack = 0, #1 byte for if_ack.
                            #ack = 1 -> if acknowledgement, 0 otherwise
                            #additional 1 byte of dummy values
                window_size = 0, #2 bytes
                checksum = 0, #2 bytes
                urgent_pointer = 0, #2 bytes
                ):
            return src_port.to_bytes(2) + \
                   dest_port.to_bytes(2) + \
                   seq.to_bytes(4) + \
                   ack.to_bytes(4) + \
                   if_ack.to_bytes(1) + \
                   (0).to_bytes(1) + \
                   window_size.to_bytes(2) + \
                   checksum.to_bytes(2) + \
                   urgent_pointer.to_bytes(2)
    


#will return a tuple
# (seq_number,ack_number, if_ack,window_size)

def retrieve_header(header):
    return \
        int.from_bytes(header[4:8]),\
        int.from_bytes(header[8:12]),\
        int.from_bytes(header[13:13]),\
        int.from_bytes(header[15:16]),\



header = create_header(seq = 3,ack = 8,if_ack=0,window_size=7)

print(header + "hello wi work".encode())

print(retrieve_header(header))