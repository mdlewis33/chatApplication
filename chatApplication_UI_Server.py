from tkinter import *
from chatApplication_Server import *
import chatApplication_UI_Gen as uiGen

def server_win():
    serverWindow = Tk()
    serverWindow.title('Client Chat')
    serverWindow.geometry('500x400')

    serverFrame = Frame(serverWindow)
    serverFrame.pack(side=TOP, padx=10, pady=10)

    def server_init_port(serverFrame):
        uiGen.clear_frame(serverFrame)
        serverFrame.after(100, lambda: init_server_ip(serverFrame))
        serverFrame.after(200, lambda: init_server_port(serverFrame))



    ipBtn = Button(serverFrame, text='Initialize server', bd=3, command=lambda: server_init_port(serverFrame))
    ipBtn.pack(side=TOP, pady=10)

    serverWindow.mainloop()
