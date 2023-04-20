from tkinter import *

def clear_frame(frame):
   for widgets in frame.winfo_children():
       widgets.destroy()

def show_results(frame, output):
    result = Label(frame, text=output)
    result.pack()

def show_popup(msg):
    popup = Tk()
    popup.title('Error!')
    label = Label(popup, text=msg)
    label.pack()
    b1 = Button(popup, text='Okay', command=popup.destroy)
    b1.pack()
    popup.mainloop()
