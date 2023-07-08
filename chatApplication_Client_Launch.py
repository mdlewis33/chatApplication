from tkinter import *
from chatApplication_Client import *
from tkinter import ttk

clientWindow = Tk()
clientWindow.style = ttk.Style()
clientWindow.style.theme_use('alt')

clientWindow.title('Client Chat')
clientWindow.geometry('500x400')

clientFrame = ttk.Frame(clientWindow)
clientFrame.pack(side=TOP)

setup_client_Btn = ttk.Button(clientFrame, text='Initialize client', command=lambda: client_setup(clientWindow))
setup_client_Btn.pack(side=TOP)

clientWindow.mainloop()
