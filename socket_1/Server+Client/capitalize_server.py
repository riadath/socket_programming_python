import socket

s = socket.socket()
print ("Socket successfully created")
port = 1234
s.bind(('', port))
print ("socket binded to %s" %(port))
s.listen(5)
print ("socket is listening")

c, addr = s.accept()
print ('Got connection from', addr )

while True:
    #send/recieve here
    # c.send('Thank you for connecting(Akib)'.encode())
    text = c.recv(1024).decode()
    #printing the recieved string
    print("Recieved String",text)
    #converting the string to uppercase using .upper() method
    text = text.upper();
    
    #sending back the string with all letters capitalized
    c.send(text.encode())
    #_______________________