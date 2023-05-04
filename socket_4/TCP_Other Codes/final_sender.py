
import socket
import time
import os

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
window_size = 4 * recv_buffer_size
mss = 8
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, recv_buffer_size)

seq_num = 0
expected_ack_num = 0


timeout = 10
start_time = time.time()
rwnd = 50
sent_size = 0
dup_ack = 0
last_ack = 0
cwnd = mss
ssthresh = 20 * window_size
estimated_rtt = 0.5
sample_rtt = 0.5
alpha = 0.125
beta = 0.25
dev_rtt = 0.5

data = b"""We're no strangers to love
You know the rules and so do I (do I)
A full commitment's what I'm thinking of
You wouldn't get this from any other guy
I just wanna tell you how I'm feeling
Gotta make you understand
Never gonna give you up
Never gonna let you down
Never gonna run around and desert you
Never gonna make you cry
Never gonna say goodbye
Never gonna tell a lie and hurt you
We've known each other for so long
Your heart's been aching, but you're too shy to say it (say it)
Inside, we both know what's been going on (going on)
We know the game and we're gonna play it
And if you ask me how I'm feeling
Don't tell me you're too blind to see
Never gonna give you up
Never gonna let you down
Never gonna run around and desert you
Never gonna make you cry
Never gonna say goodbye
Never gonna tell a lie and hurt you"""
    
data_len = len(data)
print(data_len)

orig_start = time.time()
cnt = 0
# print(f'({cnt}, {cwnd}) [a]')
print(f'({cnt}, {dev_rtt})')
yo = []
yo.append((cnt, sample_rtt))
while True:
    curr_sent_size = 0
    while curr_sent_size < window_size and seq_num < data_len:
        send_size = min(mss, data_len - seq_num)
        client_socket.sendall(toHeader(seq_num, seq_num, 0, 0, 0, 
                calculate_checksum(data[seq_num : seq_num + send_size])) 
                              + data[seq_num : seq_num + send_size])
        curr_sent_size += send_size 
        sent_size += send_size
        seq_num += send_size
        start_time = time.time()

    
    expected_ack_num = seq_num
    ack_pkt = client_socket.recv(14)
    seqNum, ack_num, ack, sf, rwnd, chcksum = fromHeader(ack_pkt)
    
    if not sf:
        curr_time = time.time()
        sample_rtt = curr_time - start_time
        estimated_rtt = alpha * sample_rtt + (1 - alpha) * estimated_rtt
        dev_rtt = beta * abs(sample_rtt - estimated_rtt) + (1 - beta) * dev_rtt
        timeout = estimated_rtt + 4 * dev_rtt
    
    if ack_num >= data_len:
        break

    if not sf:
        print(f'Timing Updates : {estimated_rtt}, {sample_rtt}, {dev_rtt}, {timeout}')

    window_size = min(cwnd, 2 * recv_buffer_size, rwnd)

    if ack_num == last_ack:
        dup_ack += 1
    else:
        dup_ack = 0
    
    if ack_num == expected_ack_num:
        if not sf:
            if cwnd >= ssthresh:
                cwnd += mss
            else:
                cwnd = min(2 * cwnd, ssthresh)
    
    if dup_ack == 3:
        # print("Triple Duplicate ACK")
        dup_ack = 0
        ssthresh = cwnd // 2
        cwnd = mss
        seq_num = last_ack

    last_ack = ack_num

    if time.time() - start_time > timeout:
        # print("Timing Out")
        if not sf:
            ssthresh = cwnd // 2
            cwnd = mss
            seq_num = last_ack
            start_time = time.time()

    cnt += 1
    if not sf:
        print(f'{cwnd}, {window_size}, {ssthresh}')
    # print(f'({cnt}, {cwnd}) [a]')
    # yo.append((cnt, ssthresh))
    # print(f'Congestion window Size = {cwnd}')
    # print(f'Ssthreshold = {ssthresh}')

print("yooooo fin")

for x, y in yo:
    print(f'({x}, {y}) [a]')
fin_time = time.time()
total_time = fin_time - orig_start
print(f"Total Time Requried is {total_time} seconds")
print(sent_size)

client_socket.close()
