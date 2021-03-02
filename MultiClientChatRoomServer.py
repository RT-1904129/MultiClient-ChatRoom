#Instructor -Dr.Neha Karankjar
#Author name-Rishabh Tripathi(1904129)
#This is whole code of Server creation which used for connecting multiple client to server 

# All required  module imported 
from _thread import *
import threading
from datetime import datetime
import socket




count=0 #it is used for counting number of user currently using
SocketArray=[]          #it is list of Socket which will containing all Socket of Client which will using

#this function user for broadcasting to every one
def BrodCastingFunction(message,informer,name="ram"):
        if informer:
                for i in range(len(SocketArray)):
                        SocketArray[i][0].send(message.encode('utf-8'))
        else:
                message=name+" : "+message
                for i in range(len(SocketArray)):
                        if(name!=SocketArray[i][1]):
                                SocketArray[i][0].send(message.encode('utf-8'))
                
                


# thread function which allot each new socket to new thread to Server 
def threaded(connection_socket):
        global count
        while True:
                client_name=""
                # data received from client 
                data = connection_socket.recv(1024)
                #if user press quit than we will stop his threading
                if (data.decode()=="quit"):  
                        break

                # Firstly we will searching name of client which because we want it should not shown to him
                for i in range(len(SocketArray)):
                        if(SocketArray[i][0]==connection_socket):
                                client_name=SocketArray[i][1]
                # send back reversed string to client
                BrodCastingFunction(data.decode(),False,client_name) 

        count-=1
        client_name=""
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        for i in range(len(SocketArray)):
                if(SocketArray[i][0]==connection_socket):
                        client_name=SocketArray[i][1]

        #this is massage used to send every client when anyone is leaving room                
        message="Server: time="+str(current_time)+" "+client_name+" has left. Member count ="+str(count)+"\n"
        BrodCastingFunction(message,True)
        SocketArray.remove((connection_socket,client_name))
        # connection closed 
        connection_socket.close() 



def Main():
        global count
        #  create a socket for listening to new connections
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                                    # use SOCK_STREAM for TCP
                                    # use SOCK_DGRAM for UDP

        # bind it to a host and a port
        host = 'localhost'
        port = 43389  # arbitrarily chosen non-privileged port number
        s.bind((host,port))
        print("Server started...waiting for a connection from the client")
        # we can join upto max 6 client at a time after that 7th client will not join to server
        s.listen(6)
        while True: 

                # accept a connection
                #add amking new connection socket for that Client
                connection_socket, addr = s.accept()
                print("Connection initiated from ",addr) 
 
                # receive some bytes and print them
                # the argument 1024 is the maximum number of characters to be read at a time
                data = connection_socket.recv(1024)
                count+=1
                SocketArray.append((connection_socket,data.decode()))
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                message="Server: time="+str(current_time)+" "+data.decode()+" has joined. Member count ="+str(count)+"\n"
                BrodCastingFunction(message,True)

                # Start a new thread and return its identifier 
                start_new_thread(threaded, (connection_socket,)) 

        #At the end when all process complete than we will stop welcoming socket
        s.close() 

            

if __name__ == '__main__': 
        Main() 
