from socket import * # to manage connection
import threading # to manage sequence


serverHost = "127.0.0.1" #listening at
serverPort = 12000       #port we want use
serverSocket = socket(AF_INET,SOCK_STREAM)

"""
binds server to IP address at specified port
"""
serverSocket.bind((serverHost,serverPort)) 

"""
listens for active connections
 """
serverSocket.listen(5) # max queue for connection


clientSockets = [] # stores all client connections
users = [] # stores all usernames of clients



# broadcast message to all clients connected to the server
def broadcast(msg):
     for clientSocket in clientSockets:
          clientSocket.send(msg);



# handle when receiving message from client
def handleMessage(client):
     while True:
          try:
               # send message to all clients
              msg = client.recv(1024)
              broadcast(msg)
          except:
               # when connection is lost, remove client
               i = clientSockets.index(client)
               clientSockets.remove(client)
               client.close()
               # remove username also
               username = users[i]
               broadcast('\n{} left!'.format(username).encode('ascii'))
               users.remove(username)
               break



# handle when new client connects to the server
def receiveClientConnection():
     print ('The server is ready to receive...')
     while True:
          connectionSocket, addr = serverSocket.accept()
          print("{} has connected!".format(str(addr)))
          connectionSocket.send("username".encode())
          username = connectionSocket.recv(1024).decode("ascii")
          users.append(username)
          clientSockets.append(connectionSocket)
          broadcast(f"{username} has joined\n".encode("ascii"))

          # handle client individually at the same time
          thread = threading.Thread(target=handleMessage, args=(connectionSocket,))
          thread.start()



receiveClientConnection()
