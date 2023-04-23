from tkinter import *
from chatApplication_Server import *

serverWindow = Tk()
serverWindow.title('Server Chat')
serverWindow.geometry('500x400')

serverFrame = Frame(serverWindow)
serverFrame.pack(side=TOP, padx=10, pady=10)

setup_server_Btn = Button(serverFrame, text='Initialize server', bd=3, command=lambda: server_setup(serverFrame))
setup_server_Btn.pack(side=TOP, pady=10)

serverWindow.mainloop()
