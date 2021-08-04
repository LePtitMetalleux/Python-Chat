#!/usr/bin/env python3
import socket
import threading
from tkinter import *
from tkinter import font
from tkinter import ttk

FORMAT = "utf-8"

class GraphicClient():
    def __init__(self):
       
        # chat window which is currently hidden
        self.Window = Tk()
        self.Window.withdraw()
         
        # login window
        self.login = Toplevel()
        # set the title
        self.login.title("Login")
        self.login.resizable(width = False,
                             height = False)
        self.login.geometry('400x300')
        # create a Label
        self.labelHead = Label(self.login,
                       text = "Connexion au serveur",
                       justify = CENTER,
                       font = "Arial 14")
        self.labelHead.pack(padx = 5, pady = 5)

        # create a entry box for
        # tyoing the message
        self.entryPseudo = Entry(self.login,
                             font = "Arial 14",
                             width=20)
        self.entryPseudo.insert(0,'Pseudo')
        self.entryPseudo.pack(padx = 5, pady = 5)

        self.entryIP = Entry(self.login,
                             font = "Arial 14",
                             width=20)
        self.entryIP.insert(0,'127.0.0.1')
        self.entryIP.pack(padx = 5, pady = 5)

        self.entryPort = Entry(self.login,
                             font = "Arial 14",
                             width=20)
        self.entryPort.insert(0,'50000')
        self.entryPort.pack(padx = 5, pady = 5)

        self.entryPseudo.bind('<Return>',lambda event: self.goAhead(self.entryPseudo.get(), self.entryIP.get(), self.entryPort.get()))
        self.entryIP.bind('<Return>',lambda event: self.goAhead(self.entryPseudo.get(), self.entryIP.get(), self.entryPort.get()))
        self.entryPort.bind('<Return>',lambda event: self.goAhead(self.entryPseudo.get(), self.entryIP.get(), self.entryPort.get()))


        # create a Continue Button
        # along with action
        self.go = Button(self.login,
                         text = "CONNEXION",
                         font = "Arial 16",
                         command = lambda: self.goAhead(self.entryPseudo.get(), self.entryIP.get(), self.entryPort.get()))
        self.go.pack(padx = 5, pady = 5)
        self.Window.mainloop()
 
    def goAhead(self, name, ip, port):

        SERVER = ip
        PORT = int(port)
        ADDRESS = (SERVER, PORT)
        
        # Create a new client socket and connect to the server
        client = socket.socket(socket.AF_INET,
                      socket.SOCK_STREAM)
        client.connect(ADDRESS)
        
        self.login.destroy()
        
        self.layout(name, client)
        
        # the thread to receive messages
        rcv = threading.Thread(target= lambda : self.receive(client))
        rcv.start()

 # The main layout of the chat
    def layout(self, name, client):
       
        self.name = name
        # to show chat window
        self.Window.deiconify()
        self.Window.title("CHATROOM")
        self.Window.resizable(width = False,
                              height = False)
        self.Window.configure(width = 470,
                              height = 550,
                              bg = "#17202A")
        self.labelHead = Label(self.Window,
                             bg = "#17202A",
                              fg = "#EAECEE",
                              text = self.name ,
                               font = "Helvetica 13 bold",
                               pady = 5)
         
        self.labelHead.place(relwidth = 1)
        self.line = Label(self.Window,
                          width = 450,
                          bg = "#ABB2B9")
         
        self.line.place(relwidth = 1,
                        rely = 0.07,
                        relheight = 0.012)
         
        self.textCons = Text(self.Window,
                             width = 20,
                             height = 2,
                             bg = "#17202A",
                             fg = "#EAECEE",
                             font = "Helvetica 14",
                             padx = 5,
                             pady = 5)
         
        self.textCons.place(relheight = 0.745,
                            relwidth = 1,
                            rely = 0.08)
         
        self.labelBottom = Label(self.Window,
                                 bg = "#ABB2B9",
                                 height = 80)
         
        self.labelBottom.place(relwidth = 1,
                               rely = 0.825)
         
        self.entryMsg = Entry(self.labelBottom,
                              bg = "#2C3E50",
                              fg = "#EAECEE",
                              font = "Helvetica 13")
         
        # place the given widget
        # into the gui window
        self.entryMsg.place(relwidth = 0.74,
                            relheight = 0.06,
                            rely = 0.008,
                            relx = 0.011)
         
        self.entryMsg.focus()
        self.entryMsg.bind('<Return>',lambda event: self.sendButton(self.entryMsg.get(), client))
        # create a Send Button
        self.buttonMsg = Button(self.labelBottom,
                                text = "Send",
                                font = "Helvetica 10 bold",
                                width = 20,
                                bg = "#ABB2B9",
                                command = lambda : self.sendButton(self.entryMsg.get(), client))
         
        self.buttonMsg.place(relx = 0.77,
                             rely = 0.008,
                             relheight = 0.06,
                             relwidth = 0.22)
         
        self.textCons.config(cursor = "arrow")
         
        # create a scroll bar
        scrollbar = Scrollbar(self.textCons)
         
        # place the scroll bar
        # into the gui window
        scrollbar.place(relheight = 1,
                        relx = 0.974)
         
        scrollbar.config(command = self.textCons.yview)
        
        self.textCons.config(state = DISABLED)
 
    # function to basically start the thread for sending messages
    def sendButton(self, msg, client):
        if msg != '' :
            self.textCons.config(state = DISABLED)
            self.msg=msg
            self.entryMsg.delete(0, END)
            snd= threading.Thread(target = lambda : self.sendMessage(client))
            snd.start()
 
    # function to receive messages
    def receive(self, client):
        while True:
            try:
                message = client.recv(1024).decode(FORMAT)
                 
                # if the messages from the server is NAME send the client's name
                if message == 'NAME':
                    client.send(self.name.encode(FORMAT))
                else:
                    # insert messages to text box
                    self.textCons.config(state = NORMAL)
                    self.textCons.insert(END,
                                         message+"\n\n")
                     
                    self.textCons.config(state = DISABLED)
                    self.textCons.see(END)
            except:
                # an error will be printed on the command line or console if there's an error
                print("An error occured!")
                client.close()
                break
         
    # function to send messages
    def sendMessage(self, client):
        self.textCons.config(state=DISABLED)
        while True:
            message = (f"{self.name}: {self.msg}")
            client.send(message.encode(FORMAT))
            break

g = GraphicClient()