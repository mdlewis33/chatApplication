import threading
from tkinter import *

# Destroys all widgets in the frame, making the window blank
# frame = Frame in the window that displays content
def clear_frame(frame):
    if frame.winfo_exists():
        for widgets in frame.winfo_children():
            widgets.destroy()

# Displays text that is passed through as a parameter
# frame = Frame in the window that displays content
# output = Text that is outputted to the screen
def display_txt(frame, output):
    result = Label(frame, text=output)
    result.pack()

# Creates a small popup window to indicate an error
# msg = Message that is displayed in the popup window
def show_popup(msg):
    popup = Tk()
    popup.title('Error!')
    label = Label(popup, text=msg)
    label.pack()
    b1 = Button(popup, text='Okay', command=popup.destroy)
    b1.pack()
    popup.mainloop()

# Creates a label to display the message that is passed as a parameter
# frame = Frame in the window that displays content
# msg = Message that is displayed to the window
def received_msg(frame, msg):
    message_label = Label(frame, text=f'Received message: {msg}')
    message_label.pack(padx=5, pady=5)
