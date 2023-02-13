import threading

IP = ''
PORT = 4498
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
SERVER_DATA_PATH = "server_data"
dic={}
def handle_client(data, addr,server):

    print(f"[RECEIVED MESSAGE] {data} from {addr}.")
    data=data.split()
    print(data[0])
    file1 = open('dns_records.txt', 'r')
    for line in file1:
        line=line.split()
        name=line[0]
        value=line[1]
        type=line[2]
        ttl=line[3]
        if name==data[0] and type==data[1]:
            server.sendto(line.encode(FORMAT),addr)
            break
            

    


def main():
   
    print("[STARTING] Server is starting")
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind(ADDR)
    print(f"[LISTENING] Server is listening on {IP}:{PORT}.")

    while True:
        data, addr = server.recvfrom(SIZE)
        data = data.decode(FORMAT)
        thread = threading.Thread(target=handle_client, args=(data, addr,server))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

if __name__ == "__main__":
    main()