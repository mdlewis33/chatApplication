from tkinter import *
from chatApplication_UI_Server import *

# Creates a window handel server and client creation
mainWindow = Tk()
mainWindow.title('Chat Application Launcher')
mainWindow.geometry('400x300')

# Creates a window that handles the server script, then destroys the button
def start_server():
    startBtn.destroy()
    server_win()

# Creates a button to start the server window
startBtn = Button(mainWindow, text='Start Server', bd=3, compound=TOP, command=start_server)
startBtn.pack()

# Creates a button that will destroy the window
quitBtn = Button(mainWindow, text='Quit', bd=3, compound=BOTTOM, command=mainWindow.destroy)
quitBtn.pack()

mainWindow.mainloop()
