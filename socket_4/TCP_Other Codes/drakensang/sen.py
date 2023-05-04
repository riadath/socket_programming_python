
import socket
import time

def toHeader(seqNum=0, ackNum=0, ack=0, sf=0, rwnd=0, chcksum = 0):
    return seqNum.to_bytes(
        4, byteorder="little") + ackNum.to_bytes(
            4, byteorder="little") + ack.to_bytes(
                1, byteorder="little") + sf.to_bytes(
                    1, byteorder="little") + rwnd.to_bytes(
                        2, byteorder="little") + chcksum.to_bytes(
                            2, byteorder="little")

def fromHeader(segment):
    return int.from_bytes(
        segment[:4], byteorder="little"), int.from_bytes(
            segment[4:8], byteorder="little"), int.from_bytes(
                segment[8:9], byteorder="little"), int.from_bytes(
                    segment[9:10], byteorder="little"), int.from_bytes(
                        segment[10:12], byteorder="little"), int.from_bytes(
                            segment[12:14], byteorder="little")

def calculate_checksum(bytestream):
    if len(bytestream) % 2 == 1:
        bytestream += b'\x00'

    checksum = 0

    for i in range(0, len(bytestream), 2):
        chunk = (bytestream[i] << 8) + bytestream[i+1]
        checksum += chunk

        if checksum > 0xffff:
            checksum = (checksum & 0xffff) + 1

    return ~checksum & 0xffff

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('127.0.0.1', 8888)
client_socket.connect(server_address)

recv_buffer_size = 4
window_size = 2 * recv_buffer_size
mss = 8
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, recv_buffer_size)

seq_num = 0
expected_ack_num = 0

data = b'This is a sample message to test the flow control algorithm, it just needs to be long enough to test the flow control algorithm.'
data_len = len(data)

timeout = 2  # in seconds
start_time = time.time()
rwnd = 50
sent_size = 0
dup_ack = 0
last_ack = 0
cwnd = 1
ssthresh = window_size
estimated_rtt = 0.5
sample_rtt = 0.5
alpha = 0.125
beta = 0.25
dev_rtt = 0.5

while seq_num < data_len:
    curr_sent_size = 0
    while curr_sent_size < window_size and seq_num < data_len:
        send_size = min(mss, data_len-seq_num)
        client_socket.sendall(toHeader(seq_num, seq_num, 0, 0, 0, 
                calculate_checksum(data[seq_num:seq_num+send_size])) + data[seq_num:seq_num+send_size])
        # print(fromHeader(toHeader(seq_num, seq_num, 0, 0, 0, 0)))
        # print(data[seq_num:seq_num+send_size], calculate_checksum(data[seq_num:seq_num+send_size]))
        curr_sent_size += send_size 
        sent_size += send_size
        seq_num += send_size
        start_time = time.time()

    curr_time = time.time()
    
    sample_rtt = curr_time - start_time
    estimated_rtt = alpha * sample_rtt + (1 - alpha) * estimated_rtt
    dev_rtt = beta * abs(sample_rtt - estimated_rtt) + (1 - beta) * dev_rtt
    timeout = estimated_rtt + 4 * dev_rtt
    
    expected_ack_num = seq_num
    ack_pkt = client_socket.recv(14)
    seqNum, ack_num, ack, sf, rwnd, chcksum = fromHeader(ack_pkt)

    window_size = min(cwnd, 2 * recv_buffer_size, rwnd)

    print(ack_num, last_ack, dup_ack)
    if ack_num == last_ack:
        dup_ack += 1
    else:
        dup_ack = 0
    
    if ack_num == expected_ack_num:
        cwnd += mss
        if cwnd >= ssthresh:
            cwnd += mss * mss // cwnd
    
    if dup_ack == 3:
        dup_ack = 0
        ssthresh = cwnd // 2
        cwnd = mss
        seq_num = last_ack

    print("cwnd,ssthres:",cwnd,ssthresh)
    
    last_ack = ack_num

    if time.time() - start_time > timeout:
        ssthresh = cwnd // 2
        cwnd = mss
        seq_num = last_ack
        print("timeout")
        start_time = time.time()


client_socket.close()
