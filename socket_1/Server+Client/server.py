import socket


#Set listener
s = socket.socket()
print ("Socket successfully created")
port = 1234
s.bind(('', port))
print ("socket binded to %s" %(port))
s.listen(5)
print ("socket is listening")
c, addr = s.accept()
print ('Got connection from', addr )



fin = open("accounts.txt","r")
account_list = []
for i in fin.readlines():
    account_list.append(i.strip().split(','))

print(account_list)

# print(account_list)
while True:
    #send/recieve here
    c.send('Enter Your Account Name : '.encode())
    account_name = c.recv(1024).decode()
    c.send('Enter Your Account Pin : '.encode())
    pincode = c.recv(1024).decode()
    #verify account
    verification_status = False
    account_info = []
    for acc in account_list:
        if acc[0] == account_name and acc[1] == pincode:
            verification_status = True
            account_info = acc 
            break
    #if verification is successfull show prompt
    if verification_status:
        menu_prompt = """
                Enter the commands below:
                1. check -> check your account balance
                2. withdraw -> withdraw from your account
                3. deposit -> deposit money to your account
                3. exit -> to exit the menu
            """
        c.send(f"Successfully Logged in \n {menu_prompt}".encode())
        
        while True:
            command = c.recv(1024).decode()
            if command == 'check':
                c.send(f'Current balance is {account_info[2]}'.encode())
            elif command == 'exit':
                #saving data to file
                for i in range(0,len(account_list)):
                    if account_list[i][0] == account_info[0]:
                        account_list[i] = account_info
                        break
                print(account_list)
                fout = open("accounts.txt","w")
                for acc in account_list:
                    fout.write(f'{acc[0]},{acc[1]},{acc[2]}\n') 
                break

            elif command == 'deposit' or command == 'withdraw':
                c.send("Enter Ammount : ".encode())
                ammount = c.recv(1024).decode()
                if command == 'deposit':
                    new_amt = int(account_info[2]) + int(ammount)
                    account_info[2] = str(new_amt)
                    c.send(f'New balance is {account_info[2]}'.encode())
                elif command == 'withdraw':
                    cur_balance = int(account_info[2])
                    if cur_balance >= int(ammount):
                        cur_balance -= int(ammount)
                        account_info[2] = str(cur_balance)
                        c.send(f'New balance is {account_info[2]}'.encode())
                    else: 
                        c.send('Insufficient Balance'.encode())

            else:
                c.send('Enter a valid command'.encode())
        
    else:
        c.send("Incorrect account name/pin\n".encode())

      