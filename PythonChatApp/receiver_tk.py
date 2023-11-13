import socket
import tkinter as tk
import threading
import random as rnd
import socket
from _thread import *

def create_header(
        src_port=88,  #2 bytes
        dest_port=88,  #2 bytes
        seq=0,  #4 bytes 
        ack=0,  #4 bytes
        if_ack=0,  #ack = 1 -> if acknowledgement, 0 otherwise
        syn=0,  #syn = 1-> if synch req
        rwnd=0,  #2 bytes
        checksum=0,  #2 bytes
        urgent_pointer=0,  #2 bytes
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


#will return a tuple - > (seq_number, ack_number, if_ack, syn, rwnd,urget_pointer)
def retrieve_header(header):
    return \
        int.from_bytes(header[4:8]),\
        int.from_bytes(header[8:12]),\
        int.from_bytes(header[12:13]),\
        int.from_bytes(header[13:14]),\
        int.from_bytes(header[14:16]),\


def send_data(connection, file_data):
    #connection establishment
    FILE_END = len(file_data)
    HEADER_SIZE = 20

    connection.settimeout(1)
    max_seg_size = 4
    file_pointer = 0
    cur_seq = 0
    rwnd = 200
    while True:
        # print("seq:", cur_seq, "rwnd:", rwnd)
        u_ptr = 0
        while rwnd >= max_seg_size:
            try:
                # print("seq:", cur_seq, "rwnd:", rwnd)
                if cur_seq + max_seg_size >= FILE_END:
                    to_send = file_data[cur_seq:FILE_END]
                    connection.send(
                        create_header(seq=cur_seq, urgent_pointer=2) + to_send)
                    file_pointer += max_seg_size

                    rwnd -= max_seg_size
                    cur_seq += max_seg_size

                    break
                else:
                    to_send = file_data[cur_seq:(cur_seq + max_seg_size)]
                    u_ptr = 0 if rwnd - max_seg_size >= max_seg_size else 1

                    connection.send(
                        create_header(seq=cur_seq, urgent_pointer=u_ptr) +
                        to_send)
                    file_pointer += max_seg_size

                    rwnd -= max_seg_size
                    cur_seq += max_seg_size

                while u_ptr == 1:
                    # print("waiting for ack")
                    try:
                        seq, ack, if_ack, syn, rwnd = retrieve_header(
                            connection.recv(HEADER_SIZE))
                        cur_seq = ack
                        u_ptr = 0
                        break
                    except Exception as e:
                        continue

            except Exception as e:
                break

        if cur_seq >= FILE_END:
            break

    print("Data sent successfully")


def receive_data(connection):
    print("Data receiving started")
    HEADER_SIZE = 20
    CONST_rwnd = 200

    connection.settimeout(1)

    max_seg_size = 4
    recv_data = b''
    expected_seq = 0
    rwnd = CONST_rwnd
    urgent_pointer = 0

    seq, ack, data = 0, 0, b''
    while True:
        try:
            if urgent_pointer == 1:
                rwnd += rnd.randint(5,7) * max_seg_size
                rwnd = min(rwnd, CONST_rwnd)
                while urgent_pointer == 1:
                    try:
                        connection.send(create_header(
                            seq=seq,
                            ack=expected_seq + max_seg_size,
                            rwnd=rwnd
                        ))
                        urgent_pointer = 0
                        break
                    except Exception as e:
                        # print('<<<',e)
                        continue
            header = connection.recv(HEADER_SIZE)
            urgent_pointer = int.from_bytes(header[18:20])
            seq, ack, if_ack, syn, window_size = retrieve_header(header)

            data = connection.recv(max_seg_size)

            recv_data += data
            # print("urgent pointer",urgent_pointer,"seq:", seq, "ack:", ack, "rwnd:", rwnd, "data:",
            #       data.decode())

            rwnd -= max_seg_size
            expected_seq += max_seg_size

            
            
            if urgent_pointer == 2:
                break

        except Exception as e:
            
            try:
                connection.send(create_header(
                                seq=seq,
                                ack=expected_seq + max_seg_size,
                                rwnd=rwnd
                            ))
                urgent_pointer = 0
            except:
                pass
            # print('>>>',e)
            pass

    print(recv_data,'End of data transfer')
    return recv_data


class ClientGUI:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = None
        
        # create the GUI
        self.root = tk.Tk()
        self.root.title("Chat App")
        
        # create the message frame
        message_frame = tk.Frame(self.root)
        message_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # create the messages label
        messages_label = tk.Label(message_frame, text="S2", font=("Arial", 14, "bold"))
        messages_label.pack(pady=(0,10))
        
        # create the messages text widget
        self.messages = tk.Text(message_frame, height=15, font=("Arial", 12))
        self.messages.pack(fill=tk.BOTH, expand=True)
        
        # create the input frame
        input_frame = tk.Frame(self.root)
        input_frame.pack(fill=tk.BOTH, expand=False, padx=10, pady=10)
        
        # create the input label
        input_label = tk.Label(input_frame, text="Enter Message", font=("Arial", 14, "bold"))
        input_label.pack(side=tk.LEFT, padx=(0,10))
        
        # create the input entry widget
        self.entry = tk.Entry(input_frame, width=40, font=("Arial", 12))
        self.entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # create the send button
        self.send_button = tk.Button(input_frame, text="Send", font=("Arial", 12, "bold"), bg="blue", fg="white", command=self.send_message)
        self.send_button.pack(side=tk.RIGHT)
        
        # bind the enter key to send the message
        self.root.bind("<Return>", lambda event: self.send_message())
        
        # connect to the server
        self.connect_to_server()

    def connect_to_server(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        self.socket.send("S2".encode())
        print("connected to server")
        threading.Thread(target=self.receive_message).start()

    def receive_message(self):
        while True:
            try:
                data = self.socket.recv(1024).decode()
                # data = receive_data(self.socket).decode()
                self.messages.insert(tk.END, 'someone else: '+data+'\n')
                self.messages.see(tk.END)
            except:
                
                continue

    def send_message(self):
        message = self.entry.get()
        if message:
            try:
                # self.socket.send(message.encode())
                send_data(self.socket, message.encode())
            except Exception as e:
                print(e)
                self.on_close()
            self.messages.insert(tk.END, "me: {}\n".format(message))
            self.messages.see(tk.END)
            self.entry.delete(0, tk.END)

    def on_close(self):
        self.socket.close()
        self.root.destroy()


if __name__ == "__main__":
    client_gui = ClientGUI("127.0.0.1", 869)
    client_gui.root.mainloop()
