import socket
import struct
IP = '10.33.2.97'
PORT = 4498
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    message = input("Enter a message to send to the server: ")

    while True:

        client.sendto(message.encode(FORMAT), ADDR)

        msg,addr=client.recvfrom(SIZE)

        msg = struct.unpack( "hhl",msg )

        print(msg)

        # type = msg.split(",")[1]
        # first = msg.split(",")[0]

        # print(first)
        # print(type)
        break

        if type == "A":
            print("IP address of the host is:")
            print(first)
            break
        else:
            client.sendto(first.encode(FORMAT), ADDR)

if __name__ == "__main__":
    main()