from tkinter import *
import time

def clear_frame(frame):
    """ Destroys all widgets in the frame, making the window blank

    Args:
        frame (Frame): Frame in the window that displays content
    """
    if frame.winfo_exists():
        for widgets in frame.winfo_children():
            widgets.destroy()

def display_txt(frame, output):
    """ Displays text that is passed through as a parameter

    Args:
        frame (Frame): Frame in the window that displays content
        output (String): Text that is outputted to the screen
    """
    result = Label(frame, text=output)
    result.pack()

def show_popup(msg):
    """ Creates a small popup window to indicate an error

    Args:
        msg (String): Message that is displayed in the popup window
    """
    popup = Tk()
    popup.title('Error!')
    label = Label(popup, text=msg)
    label.pack()
    b1 = Button(popup, text='Okay', command=popup.destroy)
    b1.pack()
    popup.mainloop()

def received_msg(frame, msg):
    """ Creates a label to display the message that is passed as a parameter

    Args:
        frame (Frame): Frame in the window that displays content
        msg (String): Message that is displayed to the window
    """
    message_label = Label(frame, text=f'Received message: {msg}')
    message_label.pack(padx=5, pady=5)

def self_end_server(frame, connection_socket, username):
    """ Ends the connection between the server and client when the script that calls this function starts
            the end of the chat and then sends a message to inform the other script to end as well

    Args:
        frame (Frame): Frame in the window that displays content
        connection_socket (socket): Connection socket used to communicate with the client
        username (String): Username of the one who ended the connection
    """

    # Clears the current frame
    clear_frame(frame)

    # Creates a label to display the username and display it with the " left the chat" message
    leave_msg = Label(frame, text="[" + username + "]" + " left the chat")
    leave_msg.pack(padx=4, pady=5)

    # Creates a label to show that the connection will be shutting down
    closing_msg = Label(frame, text="Shutting down connection...")
    closing_msg.pack(padx=5, pady=5)

    # Updates the window to show the new label
    frame.update()

    # Informs the other script to end
    connection_socket.send("end".encode())

    # Closes the connection 
    connection_socket.close()

    # Waits 5 seconds
    time.sleep(5)
    
    # Destroys the entire window
    frame.winfo_toplevel().destroy()
    
def other_end_client(serverFrame, connection_socket, username):
    """ Ends the connection between the server and client when the other script starts the end of the chat

    Args:
        serverFrame (Frame): Frame in the window that displays content
        connection_socket (socket): Connection socket used to communicate with the client
        username (String): Username of the one who ended the connection
    """

    # Clears the current frame
    clear_frame(serverFrame)

    # Creates a label to display the username and display it with the "left the chat" message
    leave_msg = Label(serverFrame, text="[" + username + "]" + " left the chat")
    leave_msg.pack(padx=4, pady=5)

    # Creates a label to show that the connection will be shutting down
    closing_msg = Label(serverFrame, text="Shutting down connection...")
    closing_msg.pack(padx=5, pady=5)

    # Updates the window to show the new label
    serverFrame.update()

    # Closes the connection
    connection_socket.close()

    # Waits 5 seconds
    time.sleep(5)

    # Destroys the entire window
    serverFrame.winfo_toplevel().destroy()