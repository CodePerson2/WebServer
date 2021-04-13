# Include Python's Socket Library
from socket import *
import time

# Specify Server Address
serverName = 'localhost'
serverPort = 80

# Create TCP Socket for Client
clientSocket = socket(AF_INET, SOCK_STREAM)

# Connect to TCP Server Socket
clientSocket.connect((serverName,serverPort))

# Test code 200
print("Testing code 200:")
sentence = "GET /index.html HTTP1.1\r\n"
clientSocket.send(sentence.encode())
modifiedSentence = clientSocket.recv(1024)
print('Reply from Server: ', modifiedSentence.decode())
clientSocket.close()
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))

# Test code 304
print("\nTesting code 304:")
# Returns 304
sentence = "GET /304.html HTTP1.1\r\nIf-Modified-Since: Fri, 6 Apr 2021 20:00:00 GMT\r\n"
clientSocket.send(sentence.encode())
modifiedSentence = clientSocket.recv(1024)
print('Reply from Server: ', modifiedSentence.decode())
clientSocket.close()
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))
# Returns 200
sentence = "GET /304.html HTTP1.1\r\nIf-Modified-Since: Fri, 12 Apr 2021 23:00:00 GMT\r\n"
clientSocket.send(sentence.encode())
modifiedSentence = clientSocket.recv(1024)
print('Reply from Server: ', modifiedSentence.decode())
clientSocket.close()
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))

# Test code 400
print("\nTesting code 400:")
# GOT instead of GET
sentence = "GOT /index.html HTTP1.1\r\nIf-Modified-Since: Fri, 6 Apr 2021 20:26:00 GMT\r\n"
clientSocket.send(sentence.encode())
modifiedSentence = clientSocket.recv(1024)
print('Reply from Server: ', modifiedSentence.decode())
clientSocket.close()
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))
# HTTP1.0 instead of 1.1
sentence = "GET /index.html HTTP1.0\r\n"
clientSocket.send(sentence.encode())
modifiedSentence = clientSocket.recv(1024)
print('Reply from Server: ', modifiedSentence.decode())
clientSocket.close()
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))

# Test code 404
print("\nTesting code 404:")
sentence = "GET /doesnotexist.html HTTP1.1\r\n"
clientSocket.send(sentence.encode())
modifiedSentence = clientSocket.recv(1024)
print('Reply from Server: ', modifiedSentence.decode())
clientSocket.close()
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))

# Test code 408
print("\nTesting code 408:")
# Reply sent within timeout time
sentence = "GET /index.html"
clientSocket.send(sentence.encode())
time.sleep(1)
sentence = " HTTP1.1\r\nIf-Modified-Since: Fri, 6 Apr 2021 20:26:00 GMT\r\n"
clientSocket.send(sentence.encode())
modifiedSentence = clientSocket.recv(1024)
print('Reply from Server: ', modifiedSentence.decode())
clientSocket.close()
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))
# Reply not sent within timeout time
sentence = "GET /index.html"
clientSocket.send(sentence.encode())
modifiedSentence = clientSocket.recv(1024)
print('Reply from Server: ', modifiedSentence.decode())
clientSocket.close()