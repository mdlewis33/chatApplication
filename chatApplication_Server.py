from socket import *
import time
import re
from tkinter import *
import chatApplication_UI_Gen as uiGen

# Creates three entry boxes for the servers' username, port, and IP address.
#   Also creates a button that once clicked will submit all typed-in answers from the entry boxes
# serverFrame = Frame in the window that displays content
def server_setup(serverFrame):
    # Initialize variables for later use
    global server_port_entry
    global server_user_entry
    global server_ip_entry

    uiGen.clear_frame(serverFrame)

    # Creates a label widget for the server IP address
    server_ip_label = Label(serverFrame, text='Enter the server IP address (Leave blank for localhost):')
    server_ip_label.pack(padx=5, pady=5, side=TOP)

    # Creates a frame for the server IP entry and button
    ip_entry_frame = Frame(serverFrame)
    ip_entry_frame.pack(padx=5, pady=5, side=TOP)

    # Creates an entry widget for the server IP address
    server_ip_entry = Entry(ip_entry_frame)
    server_ip_entry.pack(side=LEFT)

    # Creates a label widget for the server port
    server_port_label = Label(serverFrame, text='Enter the server port number (Leave blank for localhost): ')
    server_port_label.pack(padx=5, pady=5, side=TOP)

    # Creates a frame for the server ports entry and button
    port_entry_frame = Frame(serverFrame)
    port_entry_frame.pack(padx=5, pady=5, side=TOP)

    # Creates an entry widget for the server port address
    server_port_entry = Entry(port_entry_frame)
    server_port_entry.pack(side=LEFT)

    # Creates a label widget for the server username
    server_user_label = Label(serverFrame, text='Enter your username (Leave blank for server): ')
    server_user_label.pack(padx=5, pady=5, side=TOP)

    # Creates a frame for the server usernames entry and button
    user_entry_frame = Frame(serverFrame)
    user_entry_frame.pack(padx=5, pady=5, side=TOP)

    # Creates an entry widget for the server port
    server_user_entry = Entry(user_entry_frame)
    server_user_entry.pack(side=LEFT)

    # Creates a button that when clicked starts the on_ok button function
    okBtn = Button(serverFrame, text='OK', bd=3, command=lambda: on_ok(serverFrame))
    okBtn.pack(side=TOP)

# Gets the answers entered into the entry's and save them into variables.
# serverFrame = Frame in the window that displays content
def on_ok(serverFrame):
    global server_ip
    global server_port
    global server_username

    # Regular expression statement to test
    regex = "^([0-9]{1,3}\.)([0-9]{1,3}\.){2}([0-9]{1,3})$"

    # Gets the inputted server ip from the server_ip_entry entry box
    server_ip = server_ip_entry.get().strip()

    # Checks the server ip to see if it's empty, if so sets it to the default ip address (127.0.0.1)
    if server_ip == '':
        server_ip = '127.0.0.1'
    # Checks if the ip address matches the regular expression, if not creates a popup saying the ip was invalid
    if not re.search(regex, server_ip):
        # uiGen.display_txt(serverFrame, server_ip)
        uiGen.show_popup("Invalid IP Address.")

    # Gets the inputted server port from the server_port_entry entry box
    server_port = server_port_entry.get().strip()

    # Checks if the server port is empty, if so sets it to the default port number (8000)
    if server_port == '':
        server_port = 8000
    #uiGen.display_txt(serverFrame, server_port)

    # Gets the inputted server username from the server_user_entry
    server_username = server_user_entry.get().strip()

    # Checks if the server username is empty, if so sets it to the default server username (server)
    if server_username == '':
        server_username = 'server'
    #uiGen.display_txt(serverFrame, server_username)

    # Calls function to begin connection of server to client
    init_server_connect(serverFrame)

# Clears the window and attempts to connect to the client server, if it connects it will display the recieved message
# serverFrame = Frame in the window that displays content
# server_ip = Servers IP address
# server_port = Servers port number
def init_server_connect(serverFrame):
    # Clears the window
    uiGen.clear_frame(serverFrame)

    # Create server socket
    server_socket = socket(AF_INET, SOCK_STREAM)

    # Bind server socket to ip and port
    server_socket.bind((server_ip, int(server_port)))

    # Listen for incoming connections
    server_socket.listen()

    # Creates a label that shows the server is waiting for a connection to the client
    connect_label = Label(serverFrame, text='Trying to connect to another user...')
    connect_label.pack(padx=5, pady=5)

    # Updates the frame to show the previous label
    serverFrame.update()

    # Create connection socket
    connection_socket, address = server_socket.accept()

    # Receive the client username from the server
    global client_username

    client_username = connection_socket.recv(2048).decode()

    connection_socket.send(server_username.encode())

    # Edits previous label new message once server is connected
    connect_label.config(text='Connection established.')

    # Updates the window to show the new label
    serverFrame.update()

    # Calls function to receive a message from the client
    receive_client(serverFrame, connection_socket)

# Receives a message from the client and prints it to the frame
# serverFrame = Frame in the window that displays content
# connection_socket = Connection socket used to communicate with the server
# c_user = Clients username
def receive_client(serverFrame, connection_socket):
    # Creates a frame to put the client information into
    connect_frame = Frame(serverFrame)
    connect_frame.pack(padx=5, pady=5, side=TOP)

    # Creates a label that displays a message
    connect_label = Label(connect_frame, text='Waiting for client to send a message...')
    connect_label.pack(padx=5, pady=5)

    # Updates the window to show the new label
    connect_frame.update()

    # Message received from the client server
    client_message = connection_socket.recv(2048).decode()

    if client_message.lower() == "end":
        server_end_client(connect_frame, connection_socket)

    # Modified client message to include the username and time
    client_message = "<" + time.asctime(time.localtime()) + "> " + "[" + client_username + "]: " + client_message

    # Destroys previous label to allow for new label
    connect_label.destroy()

    # Creates a new label that displays the client message
    client_message_label = Label(connect_frame, text=client_message)
    client_message_label.pack(padx=5, pady=5)

    # Starts the function to start the sending process to the client
    send_to_client(connect_frame, connection_socket)

# Displays an entry box that holds the message that will be sent to the client, activated with the click of the button
# serverFrame = Frame in the window that displays content
# connection_socket = Connection socket used to communicate with the server
def send_to_client(serverFrame, connection_socket):
    global server_msg_entry

    # Creates a frame to enter information from the entry
    msg_entry_frame = Frame(serverFrame)
    msg_entry_frame.pack(padx=5, pady=5, side=TOP)

    # Creates a label widget for the server message
    server_msg_label = Label(msg_entry_frame, text='Enter a message to send to the client:')
    server_msg_label.pack(padx=5, pady=5, side=TOP)

    # Creates an entry widget for the server message
    server_msg_entry = Entry(msg_entry_frame)
    server_msg_entry.pack(padx=5, side=LEFT)

    # Creates a button that when clicked starts the on_ok_msg button function
    okBtn = Button(msg_entry_frame, text='OK', bd=3, command=lambda: on_ok_msg(msg_entry_frame, connection_socket))
    okBtn.pack(padx=5, side=LEFT)

# Gets the message and deletes the input text and box with the output and sends the message to the client
# msg_frame = Frame in the window that displays content
# connection_socket = Connection socket used to communicate with the server
def on_ok_msg(msg_frame, connection_socket):

    # Gets a message from the window
    send_server_message = server_msg_entry.get().strip()

    # Checks to see if the message is empty and if so, displays a popup window
    if send_server_message == "":
        uiGen.show_popup("Invalid Input!")
    if send_server_message.lower() == "end":
        server_end_server(msg_frame, connection_socket)

    # Sets the server message to the input from the entry with the server username and time added on
    server_message = "<" + time.asctime(time.localtime()) + "> " + "[" + server_username + "]: " + send_server_message

    # Clears the current frame
    uiGen.clear_frame(msg_frame)

    # Creates a label to display the client message to the window
    server_message_label = Label(msg_frame, text=server_message)
    server_message_label.pack(padx=5, pady=5)

    # Sends the client message to the client
    connection_socket.send(send_server_message.encode())

    # Starts the function to begin receiving from the client script
    receive_client(msg_frame, connection_socket)

def server_end_server(serverFrame, connection_socket):

    uiGen.clear_frame(serverFrame)

    leave_msg = Label(serverFrame, text="[" + server_username + "]" + " left the chat")
    leave_msg.pack(padx=4, pady=5)

    closing_msg = Label(serverFrame, text="Shutting down connection...")
    closing_msg.pack(padx=5, pady=5)

    # Update the window to display the new labels
    serverFrame.update()

    connection_socket.send("end".encode())

    connection_socket.close()

    time.sleep(5)

    serverFrame.winfo_toplevel().destroy()

def server_end_client(serverFrame, connection_socket):

    uiGen.clear_frame(serverFrame)

    leave_msg = Label(serverFrame, text="[" + client_username + "]" + " left the chat")
    leave_msg.pack(padx=4, pady=5)

    closing_msg = Label(serverFrame, text="Shutting down connection...")
    closing_msg.pack(padx=5, pady=5)

    # Update the window to display the new labels
    serverFrame.update()

    connection_socket.close()

    time.sleep(5)

    serverFrame.winfo_toplevel().destroy()
