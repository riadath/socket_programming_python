import socket
from dnslib.dns import *
SERVER_PORT = ('127.0.0.1',1969)
BUFFER = 1024

def main():
    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    while True:
        dns_query = input("Enter Domain : ")
        question = DNSRecord.question(dns_query).pack()
        ip_address = ""
        while True:
            UDPClientSocket.sendto(question,SERVER_PORT)
            message,addr = UDPClientSocket.recvfrom(BUFFER)
            
            message = DNSRecord.parse(message)
            message = str(message.get_a()).split()

            response,res_type = message[4],message[3]

            if res_type == 'A' or res_type == 'AAAA':
                
                ip_address = response
                break
            else:
                print(response," << Redirecting")
                question = DNSRecord.question(response).pack()

        print("IP Address : ",ip_address)

if __name__ == "__main__":
    main()