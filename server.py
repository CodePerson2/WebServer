# Include Python's Socket Library
from socket import *

# Specify Server Port
serverPort = 12000

# Create TCP welcoming socket
serverSocket = socket(AF_INET,SOCK_STREAM)

# Bind the server port to the socket
serverSocket.bind(('',serverPort))

# Server begins listerning foor incoming TCP connections
serverSocket.listen(1)
print ('The server is ready to receive')

while True: # Loop forever
     # Server waits on accept for incoming requests.
     # New socket created on return
     connectionSocket, addr = serverSocket.accept()
     
     # Read from socket (but not address as in UDP)
     sentence = connectionSocket.recv(1024).decode()
     print(sentence)
     # Send the reply
     connectionSocket.send(('HTTP/1.1 200 OK\n').encode())      #1.0 should work as well
     connectionSocket.send(('Content-Type: text/html\n').encode())
     connectionSocket.send(('\n').encode()) # header and body should be separated by additional newline
     connectionSocket.send(("""
        <html>
        <body>
        <h1>Shit works</h1> yeeee
        </body>
        </html>
    """).encode())
     
     # Close connectiion too client (but not welcoming socket)
     connectionSocket.close()