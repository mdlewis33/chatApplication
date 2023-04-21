from tkinter import *
from chatApplication_Server import *
import chatApplication_UI_Gen as uiGen

# Creates a server window with a button that when pressed starts the servers setup
def server_win():
    serverWindow = Tk()
    serverWindow.title('Client Chat')
    serverWindow.geometry('500x400')

    serverFrame = Frame(serverWindow)
    serverFrame.pack(side=TOP, padx=10, pady=10)

    ipBtn = Button(serverFrame, text='Initialize server', bd=3, command=lambda: server_setup(serverFrame))
    ipBtn.pack(side=TOP, pady=10)

    serverWindow.mainloop()
