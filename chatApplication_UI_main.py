from tkinter import *
from chatApplication_UI_Server import *

mainWindow = Tk()
mainWindow.title('Chat Application Launcher')
mainWindow.geometry('400x300')

def start_server():
    btn1.destroy()
    server_win()

btn1 = Button(mainWindow, text='Start Server', bd=3, command=start_server)
btn1.pack()

mainWindow.mainloop()