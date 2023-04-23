from tkinter import *
from chatApplication_Client import *

clientWindow = Tk()
clientWindow.title('Client Chat')
clientWindow.geometry('500x400')

clientFrame = Frame(clientWindow)
clientFrame.pack(side=TOP, padx=5, pady=10)

setup_client_Btn = Button(clientFrame, text='Initialize client', bd=3, command=lambda: client_setup(clientWindow))
setup_client_Btn.pack(side=TOP, pady=10)

clientWindow.mainloop()
