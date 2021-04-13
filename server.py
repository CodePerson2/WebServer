# Include Python's Socket Library
from socket import *
from datetime import *
import threading
import sys
import os.path


# Specify Server Port
# Port 80 is the defacto http port
# access the server by using http://localhost or http://localhost/index.html
serverPort = 80

# Create TCP welcoming socket
serverSocket = socket(AF_INET, SOCK_STREAM)


def sendHtml(connectionSocket, resp, lastModified, fileData):
    #d = datetime.now()
    # print(d)

    responseString = '';
    if resp == '200':
        responseString += 'HTTP/1.1 200 OK\r\n'
        responseString += 'max-age=60\r\n'
        responseString += 'Cache-Control: no-cache\r\n'
        responseString += 'Content-Type: text/html\r\n'
        responseString += 'HTTP/1.1 200 OK\r\n'

        # Last-Modified: Fri, 9 Apr 2021 20:26:00 GMT\r\n
        # header and body should be separated by additional newline
        responseString += '\r\n'
        responseString +=  fileData
        connectionSocket.send((responseString).encode())

    elif resp == '404':
        connectionSocket.send(('HTTP/1.1 404 Not Found\r\n').encode()
                              )
    elif resp == '304':
        datenow = datetime.strftime(datetime.now(), "%a, %d %b %Y %H:%M:%S %Z")
        # Made the reply into one string before sending it because I was having trouble
        # receiving all of it at client.py
        reply = 'HTTP/1.1 304 Not Modified\r\nDate: ' + datenow + '\r\n'
        connectionSocket.send(reply.encode()
                              )
    elif resp == '400':
        connectionSocket.send(('HTTP/1.1 400 Bad Request\r\n').encode()
                              )
    elif resp == '408':
        connectionSocket.send(('HTTP/1.1 408 Request Timed Out\r\n').encode()
                              )

    # Close connectiion too client (but not welcoming socket)
    connectionSocket.close()

# handles making the connection, uses sendHtml() to return webpage
def makeConnection(connectionSocket, addr):

    # Read from socket (but not address as in UDP)
    sentence = connectionSocket.recv(1024).decode()
    req = sentence.split('\r\n')
    location = req[0].split(' ')
    print('\n' + sentence)
    print('req: ', req)
    print('\nlocation: ', location)
    resp = '200'

    # Find if there is a If-Modified-Since in the request
    ifModifiedSinceFlag = False
    ifModifiedSince = ''

    # Check if any lines in the request begin with If-Modified-Since
    for line in req:
        if line.find('If-Modified-Since: ') != -1:
            ifModifiedSinceFlag = True
            ifModifiedSince = line[19:len(line)]
            print('If-Modified-Since: ' + ifModifiedSince)        

    if len(location) < 3:
        # 408 Request Timed Out, could try to read again from the socket, but use a non-blocking call with a timeout
        resp = '408'
        print('Request Timed Out')
        sendHtml(connectionSocket, resp, '', '')

    # Check if the HTML file exists locally
    if location[1] == '/':
        filePath = './index.html'
    else:
        filePath = '.' + location[1]
    fileData = ''
    fileLastModified = datetime.now()
    fileExists = False
    if os.path.exists(filePath):
        # Check if it is a directory and update the path
        if os.path.isdir(filePath):
            if location[1] == '/':
                filePath = filePath + '/index.html'
            else:
                filePath = filePath + location[1]
        # Check the file still exists if the first one was a directory
        # Extract the last modified date and HTML
        if os.path.exists(filePath):
            fileExists = True
            fileLastModified = os.path.getmtime(filePath)
            fileLastModified = datetime.fromtimestamp(fileLastModified)
            print(fileLastModified)
            fp = open(filePath)
            data = fp.readlines()
            fp.close()
            
            fileData = data[0]
            for i in range(1,len(data)):
                fileData = fileData + data[i]
            print("File exists locally: ", filePath)
            print(fileLastModified)
            print(fileData)

    if location[0] != 'GET' and location[2] != 'HTTP/1.1\r\n' or len(location) != 3:
        # 400 Bad request, checked first in case the request is incorrect
        resp = '400'
        print("Bad request")
    elif ifModifiedSinceFlag and fileExists:
        # 304 Not Modified
        ifModifiedSinceTime = datetime.strptime(
            ifModifiedSince, "%a, %d %b %Y %H:%M:%S %Z")

        print(ifModifiedSinceTime)
        # Using datetime.now(), needs to be updated
        if ifModifiedSinceTime < fileLastModified:
            resp = '304'
        print("Not Modified")
    elif fileExists:
        # 200 OK
        print('true')
    else:
        # 404 Not Found
        resp = "404"
        print("Not Found")
    # Send the reply
    sendHtml(connectionSocket, resp, fileLastModified, fileData)


# Bind the server port to the socket
serverSocket.bind(('', serverPort))

# Server begins listerning foor incoming TCP connections
serverSocket.listen(1)
print('The server is ready to receive')

try:
    while True:  # Loop forever
        # Server waits on accept for incoming requests.
        # New socket created on return
        connectionSocket, addr = serverSocket.accept()

        # create thread when server recieves connection request
        # Probably should pass through thread and end it when connection is closed
        # This now works for mutliple connections (ie: browsers/tabs open)
        th = threading.Thread(target=makeConnection,
                              args=(connectionSocket, addr))
        th.start()

    # This wasnt working for me, I commented it out jsut becasue wasnt sure where to put it
    # When I was changing the code around
    # Spam a bunch of CTRL+C and then send a HTTP request, the server will close.
    # The serverSocket.accept() is blocking, buffering a bunch of keyboard interrupts
    # allows the program to stop when the program is unblocked
except KeyboardInterrupt:
    serverSocket.close()
    print("Server is closed")
    th.join()
    sys.exit(0)
