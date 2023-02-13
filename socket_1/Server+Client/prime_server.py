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
    number = int(c.recv(1024).decode())
    print("Recieved Number : ",number)
    result = str(number) + ' is a prime.'
    for i in range(2,number):
        if i*i > number:
            break
        if number%i == 0:
            result = str(number) + ' is not a prime'
            break
    c.send(result.encode())
    #_______________________