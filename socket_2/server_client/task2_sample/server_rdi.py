
import socket
import os.path
import hashlib
import webbrowser

HTTP_PORT = 80 #HTTP port
USER_AGENT = 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36 Edg/97.0.1072.76'
#This method gets rid of Header information and only keeps the html document part
#idea is keep skipping until we find a string that starts with <html , since all html documents contain that
#from there, we keep concatinating all the strings and then return it
def skipUntilDoc(string):
    list = string.split('\n')
    flag = False
    ans = ''
    for line in list:
        listItem = line.split(' ', maxsplit=1)
        if (listItem[0].lower().startswith('<html')):
            flag = True
        if(flag):
           ans += line + '\n'

    return ans


def findIfModified(string,fileName): #return false if we find the same timestamp

    file = open(f"{fileName}.txt", "r") #open file
    flag = 0
    index = 0
    ans : string
    for line in file:

        if string in line:
            file.close()
            return False

    file.close()
    return True

#this one takes in the Header information as a string
#it returns the timestamp if there is one provided.
# Otherwise it returns an empty string
def findTime(string):
    list = string.split('\n')
    for line in list:
        listItems = line.split(' ',maxsplit=1)
        if(listItems[0] == 'Last-Modified:'):
            return listItems[1]

    return ''
#This is the main method for the GET/HEAD request
def getIt(core,fileName,flag):

    list = core.split('/', maxsplit=1) #Split url into, path and domain
    val1 = 'HEAD'
    val2 = 'GET'
    val3 = val1 if(flag==True)  else val2 #our flag determines what kind of HTTP request are we doing
    #This is the req format
    req = f'{val3} /{list[1]} HTTP/1.1\r\n' \
          f'Host: {list[0]}:80\r\n' \
          f'User-agent: {USER_AGENT}\r\n' \
          f'Connection: close\r\n' \
          f'\r\n'
    #We latch it in try catch loop as it can fail
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as skt: #closes socket after a connection
            print('Socket created.')
            skt.connect((list[0], HTTP_PORT)) #Connects to the desired URL/Path and port is 80
            skt.sendall(req.encode()) #Send the request based on flag, either GET or HEAD

            header = b'' #header is initially empty, this is where message will be

            while True: #Until we finish receiving data
                buffer = skt.recv(1024) #recieve 1024 bytes everytime
                if not buffer:
                    break
                header += buffer#concat the answer

        if(flag == True): #If we already have some data, cached
            timeStamp = findTime(header.decode(encoding='utf-8')) #Figure out the timestamp

            if timeStamp != '': #if time stamp exists,
                timeStamp = hashlib.md5(timeStamp.encode()) #hash it
                #we look for a key value pair (hash of url) + (hash of timestamp) in values.txt, if we cannot find it, then it is modified
                if (findIfModified(fileName.hexdigest() + timeStamp.hexdigest(), 'values') == True):  # it has been modified
                    getIt(core, fileName, False)
                else:
                    webbrowser.open_new_tab(f"{fileName.hexdigest()}.html")
            else: # No time stamp means we do query again
                getIt(core,fileName,False)

        else:
            #First write the file since it has no occurance in our cache
            file = open(f"{fileName.hexdigest()}.html", "w") #This opens the hash file.html
            toWrite = skipUntilDoc(header.decode(encoding='utf-8'))#this part writes only HTML part into that file
            file.write(toWrite) #write it
            file.close()
            #find if it has timestamp, if it does, write it down
            timeStamp = findTime(header.decode(encoding='utf-8')) #find the timestamp
            print(timeStamp)
            if timeStamp != '':
                timeStampHash = hashlib.md5(timeStamp.encode())
                print(fileName.hexdigest() + timeStampHash.hexdigest())
                file = open("values.txt", "a")
                file.write( fileName.hexdigest() + timeStampHash.hexdigest() + '\n')
                file.close()
            webbrowser.open_new_tab(f"{fileName.hexdigest()}.html")



    except socket.error as e:
        print('Socket creation failed.')


def main():
    if os.path.exists("values.txt") == False:
        file = open("values.txt", "w")
        file.close()
    ipt = input("Enter your value in this format : http://www.domain_name.com/path\n"
                "make sure to follow this format: ")
    mainUrl = ipt.split('//',maxsplit=1) #Getting rid of the http:// part
    core = mainUrl[1]  # main url part
    hashCode = hashlib.md5(core.encode()) #Hash the url for a unique identifier for the webpage
    fileName = hashCode #assign the hash value to make file
    file_exists = os.path.exists(f'{fileName.hexdigest()}.html') #If this file exists, we have previously cached it
    if file_exists == False:
        getIt(core,fileName,False)#False means we do direct GET
    else:
        getIt(core,fileName,True)#True means we do HEAD first


if __name__ == '__main__':
    main()


