#Instructor -Dr.Neha Karankjar
#Author name-Rishabh Tripathi(1904129)

#all important library installation
import socket
import tkinter as tk
from tkinter import messagebox
import threading





class UserClient :
    def __init__(self,host_ip_address,portNumber):

        self.client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        # The first argument AF_INET specifies the addressing family (IP addresses)
        # The second argument is SOCK_STREAM for TCP service
        #    and SOCK_DGRAM for UDP service
        self.username=""    #it will used for username
        self.client.connect((host_ip_address,portNumber))
        #here I am using Python GUI for making our work easy every variable reflect the there work so no need to explain there work  
        self.window = tk.Tk()       #initialte the window
        self.window.title("Client") 
        self.window.configure(bg="Red")
        self.topFrame = tk.Frame(self.window)
        self.lableName = tk.Label(self.topFrame, text = "Enter login name ").pack(side=tk.LEFT)
        self.enterName = tk.Entry(self.topFrame)
        self.enterName.pack(side=tk.LEFT)
        self.bottonConnect = tk.Button(self.topFrame, text="Connect to server", command=self.connect)
        self.bottonConnect.pack(side=tk.LEFT)
        self.topFrame.pack(side=tk.TOP)
        self.displayFrame = tk.Frame(self.window)
        self.scrollBar = tk.Scrollbar(self.displayFrame)
        self.scrollBar.pack(side=tk.RIGHT, fill=tk.Y)
        self.userDisplay = tk.Text(self.displayFrame, height=21, width=65)
        self.userDisplay.pack(side=tk.LEFT, fill=tk.Y, padx=(5, 0))
        self.userDisplay.tag_config("tag_your_message", foreground="blue")
        self.scrollBar.config(command=self.userDisplay.yview)
        self.userDisplay.config(yscrollcommand=self.scrollBar.set, background="#F4F6F7", highlightbackground="grey", state="disabled")
        self.displayFrame.pack(side=tk.TOP)
        self.bottomFrame = tk.Frame(self.window)
        self.takeMessage = tk.Text(self.bottomFrame, height=3, width=65)
        self.takeMessage.pack(side=tk.LEFT, padx=(5, 13), pady=(5, 10))
        self.takeMessage.config(highlightbackground="grey", state="disabled")
        self.takeMessage.bind("<Return>", (lambda event: self.getMessageSendToServer(self.takeMessage.get("1.0", tk.END))))
        self.bottomFrame.pack(side=tk.BOTTOM)
        self.window.mainloop()

    # This function used for connecting user login id to server once user type his login name it will try to connect to Client to Server   
    def connect(self):
        #if user do not type and press connet key than this error will show to him
        if len(self.enterName.get()) < 1:
            tk.messagebox.showerror(title="ERROR!!!", message="You MUST enter your first name <e.g. John>")
        else:
            self.username = self.enterName.get()
            self.client.send(self.username.encode('utf-8')) # Send name to server after connecting
            self.enterName.config(state=tk.DISABLED)
            self.bottonConnect.config(state=tk.DISABLED)
            self.takeMessage.config(state=tk.NORMAL)
            # start a thread to keep receiving message from server
            # do not block the main thread :)
            threading._start_new_thread(self.receive_message_from_server, (self.client,))

    #this function take messages from user and send to server        
    def getMessageSendToServer(self,message):
        message = message.replace('\n', '')
        texts = self.userDisplay.get("1.0", tk.END).strip()
        # enable the display area and insert the text and then disable.
        #Gernally tkinter does not allow user to insert into a disabled test widget
        self.userDisplay.config(state=tk.NORMAL)
        
        if(len(texts)<1):
            self.userDisplay.insert(tk.END, "You->" + message, "tag_your_message")
        else:
            self.userDisplay.insert(tk.END, "\n\n" + "You->" + message, "tag_your_message")
        self.userDisplay.config(state=tk.DISABLED)
        self.client.send(message.encode('utf-8'))
        #if user type quite than we will close the socket which connect to this user and server
        #and we will destroy that client window also of GUI
        if (message == "quit"):
            self.client.close()
            self.window.destroy()
        self.userDisplay.see(tk.END)
        self.takeMessage.delete('1.0', tk.END)

    #this function is self explanatery
    def  receive_message_from_server(self,Sockt):
        
        while True:
            from_server = Sockt.recv(1024)

            texts = self.userDisplay.get("1.0", tk.END).strip()
            self.userDisplay.config(state=tk.NORMAL)
            if len(texts) < 1:
                self.userDisplay.insert(tk.END, from_server.decode())
            else:
                self.userDisplay.insert(tk.END, "\n\n"+ from_server.decode())

            self.userDisplay.config(state=tk.DISABLED)
            self.userDisplay.see(tk.END)


def Main():
    
    # connect to the server
    host="localhost"          
    port=43389  # this is the server's port number, which the client needs to know
    client=UserClient(host,port)


if __name__ == '__main__': 
    Main()
