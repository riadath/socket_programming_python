import socket
from dnslib.dns import *

#UDP Server

SERVER_PORT = ('127.0.0.1',1969)
BUFFER = 1024

dns_records = {}
fin = open("dns_records.txt","r")
for i in fin.readlines():
    temp = i.split()
    try:
        dns_records[temp[0]].append((temp[1],temp[2],temp[3]))
    except:
        dns_records[temp[0]] = []
        dns_records[temp[0]].append((temp[1],temp[2],temp[3]))
fin.close()

# print(dns_records)

def get_queryType(qtype,value):
    if qtype == 'A':
        return QTYPE.A,A(value)
    if qtype == 'AAAA':
        return QTYPE.AAAA,AAAA(value)
    if qtype == 'MX':
        return QTYPE.MX,MX(value)
    if qtype == 'CNAME':
        return QTYPE.CNAME,CNAME(value)
    if qtype == 'NS':
        return QTYPE.NS,NS(value)

def main():
    UDPSocket = socket.socket(family=socket.AF_INET,type=socket.SOCK_DGRAM)
    UDPSocket.bind(SERVER_PORT)
    print("Server Socket Created")
    while True:
        message,addr = UDPSocket.recvfrom(BUFFER)
        message = DNSRecord.parse(message)

        #extract question
        domain_name = str(message.get_q().get_qname())
        list_lt = max(1,len(dns_records[domain_name]) - 1)
        r_rec = dns_records[domain_name][random.randrange(list_lt)]

        #create response
        response = message.reply()
        qtype,value = get_queryType(r_rec[1],r_rec[0])
        response.add_answer(
            RR(domain_name,qtype,rdata=value, ttl=int(r_rec[2]))
        )

        UDPSocket.sendto(response.pack(),addr)


if __name__ == "__main__":
    main()