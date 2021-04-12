# Include Python's Socket Library
from socket import *

# Specify Server Address
serverName = 'localhost'
serverPort = 80

# Create TCP Socket for Client
clientSocket = socket(AF_INET, SOCK_STREAM)

# Connect to TCP Server Socket
clientSocket.connect((serverName,serverPort))

# Recieve user input from keyboard
# Uncomment the case that is being tested
sentence = "GET index.html HTTP1.1\r\nIf-Modified-Since: Fri, 6 Apr 2021 20:26:00 GMT\r\n" #304
#sentence = "GET index.html"  #408
#sentence = "GOT index.html HTTP1.1\r\nIf-Modified-Since: Fri, 6 Apr 2021 20:26:00 GMT\r\n" #400

# Send! No need to specify Server Name and Server Port! Why?
clientSocket.send(sentence.encode())

# Read reply characters! No need to read address! Why?
modifiedSentence = clientSocket.recv(1024)

# Print out the received string
print ('From Server:', modifiedSentence.decode())

# Close the socket
clientSocket.close()