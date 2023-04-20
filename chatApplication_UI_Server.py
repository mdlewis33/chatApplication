from tkinter import *
from chatApplication_Server import *

def server_win():
    serverWindow = Toplevel()
    serverWindow.title('Client Chat')
    serverWindow.geometry('500x400')

    frame = Frame(serverWindow)
    frame.pack(side="top", expand=True, fill="both")

    beginBtn = Button(frame, text='Start server', bd=3, command=lambda: init_server_ip(frame))
    beginBtn.pack()

    serverWindow.mainloop()

def clear_frame(frame):
   for widgets in frame.winfo_children():
      widgets.destroy()
def show_results(frame, output):
    clear_frame(frame)

    result = Label(frame, text=output)
    result.pack()