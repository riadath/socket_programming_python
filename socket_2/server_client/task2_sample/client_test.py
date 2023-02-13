import requests
fil=input('Enter File Name: ')
x = requests.get('http://localhost:8080//Users/User/Documents/CODE_DRIVE/Networking_Lab/socket_2/server_client/files/{fil}')
if x.status_code == 200:
    with open(fil, "wb") as f:
        f.write(x.content)
    print("File successfully received")
    print("Content: ",x.text)
else:
    print("Error: Could not receive file")