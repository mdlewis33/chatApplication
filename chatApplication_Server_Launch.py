from tkinter import *
from chatApplication_Server import *
from tkinter import ttk

serverWindow = Tk()
serverWindow.style = ttk.Style()
serverWindow.style.theme_use('alt')

serverWindow.title('Server Chat')
serverWindow.geometry('500x400')

serverFrame = ttk.Frame(serverWindow)
serverFrame.pack(side=TOP)

setup_server_Btn = ttk.Button(serverFrame, text='Initialize server', command=lambda: server_setup(serverFrame))
setup_server_Btn.pack(side=TOP)

serverWindow.mainloop()
