import socket
import tkinter as tk
import threading


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
        messages_label = tk.Label(message_frame, text="Messages", font=("Arial", 14, "bold"))
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
        threading.Thread(target=self.receive_message).start()

    def receive_message(self):
        while True:
            try:
                data = self.socket.recv(1024).decode()
                self.messages.insert(tk.END, 'SERVER: '+data+'\n')
                self.messages.see(tk.END)
            except:
                break

    def send_message(self):
        message = self.entry.get()
        if message:
            try:
                self.socket.send(message.encode())
            except:
                self.on_close()
            self.messages.insert(tk.END, "CLIENT: {}\n".format(message))
            self.messages.see(tk.END)
            self.entry.delete(0, tk.END)

    def on_close(self):
        self.socket.close()
        self.root.destroy()


if __name__ == "__main__":
    client_gui = ClientGUI("127.0.0.1", 869)
    client_gui.root.mainloop()
