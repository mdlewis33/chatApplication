from socket import *
import time
import re
from tkinter import *
import chatApplication_UI_Gen as uiGen

def client_setup(clientFrame):
    """ Creates three entry boxes for the clients username, port, and IP address.
            Also creates a button that once clicked will start a function to handel the inputs, activated with the click of the button

    Args:
        clientFrame (Frame): Frame in the window that displays content
    """
    
    # Initialize variables for later use
    global client_port_entry
    global client_user_entry
    global client_ip_entry

    # Clears the current frame
    uiGen.clear_frame(clientFrame)

    # Creates a label widget for the client IP address
    client_ip_label = Label(clientFrame, text='Enter the client IP address (Leave blank for localhost):')
    client_ip_label.pack(padx=5, pady=5, side=TOP)

    # Creates a frame for the client IP entry and button
    ip_entry_frame = Frame(clientFrame)
    ip_entry_frame.pack(padx=5, pady=5, side=TOP)

    client_ip_entry = Entry(ip_entry_frame)
    client_ip_entry.pack(side=LEFT)

    # Creates a label widget for the server port
    client_port_label = Label(clientFrame, text='Enter the client port number (Leave blank for localhost): ')
    client_port_label.pack(padx=5, pady=5, side=TOP)

    # Creates a frame for the client ports entry and button
    port_entry_frame = Frame(clientFrame)
    port_entry_frame.pack(padx=5, pady=5, side=TOP)

    client_port_entry = Entry(port_entry_frame)
    client_port_entry.pack(side=LEFT)

    # Creates a label widget for the server username
    client_user_label = Label(clientFrame, text='Enter your username (Leave blank for user): ')
    client_user_label.pack(padx=5, pady=5, side=TOP)

    # Creates a frame for the server usernames entry and button
    user_entry_frame = Frame(clientFrame)
    user_entry_frame.pack(padx=5, pady=5, side=TOP)

    # Creates an entry widget for the server port
    client_user_entry = Entry(user_entry_frame)
    client_user_entry.pack(side=LEFT)

    # Creates a button that when clicked starts the on_ok button function
    okBtn = Button(clientFrame, text='OK', command=lambda: on_ok(clientFrame))
    okBtn.pack(side=TOP)

def on_ok(clientFrame):
    """ Gets the input entered from the entry's and saves them into variables

    Args:
        clientFrame (Frame): Frame in the window that displays content
    """
    
    global client_ip
    global client_port
    global client_username

    # Regular expression statement
    regex = "^([0-9]{1,3}\.)([0-9]{1,3}\.){2}([0-9]{1,3})$"

    # Gets the inputted client ip from the client_ip_entry entry box, removes whitespace from the front and back for string
    client_ip = client_ip_entry.get().strip()

    # Checks the client ip to see if it's empty, if so sets it to the default ip address (127.0.0.1)
    if client_ip == '':
        client_ip = '127.0.0.1'
    # Checks if the ip address matches the regular expression, if not creates a popup saying the ip was invalid
    if not re.search(regex, client_ip):
        uiGen.show_popup("Invalid IP Address.")

    # Gets the inputted client port from the client_port_entry entry box, removes whitespace from the front and back for string
    client_port = client_port_entry.get().strip()

    # Checks if the client port is empty, if so sets it to the default port number (8000)
    if client_port == '':
        client_port = 8000

    # Gets the inputted client username from the client_user_entry, removes whitespace from the front and back for string
    client_username = client_user_entry.get().strip()

    # Checks if the clients username is empty, if so sets it to the default client username ("user")
    if client_username == '':
        client_username = 'user'

    # Calls function to begin connection of server to client
    init_client_connect(clientFrame)

def init_client_connect(clientFrame):
    """ Clears the window and attempts to connect to the server, if it connects it will display the received message

    Args:
        clientFrame (Frame): Frame in the window that displays content
    """
    
    # Clears the current frame
    uiGen.clear_frame(clientFrame)

    # Create connection socket
    connection_socket = socket(AF_INET, SOCK_STREAM)

    # Sets the connection timeout to 5 seconds
    connection_socket.settimeout(5)

    # Creates a label that shows the client is trying to connect to the server
    connect_label = Label(clientFrame, text='Trying to connect to server...')
    connect_label.pack(padx=5, pady=5)

    # Updates the window to show the new label
    clientFrame.update()

    # Tries to connect to the server, if not then it says that the ip or port is wrong and starts from the start
    try:
        connection_socket.connect((client_ip, int(client_port)))
    except socket.error:
        uiGen.show_popup("Server IP or port is incorrect.")
        client_setup(clientFrame)

    # Sets the connection timeout to unlimited
    connection_socket.settimeout(None)

    # Waits for 1 second
    time.sleep(1)

    # Edits previous label to the new message once client is connected
    connect_label.config(text='Connection established.')

    # Sends the clients username to the server
    connection_socket.send(client_username.encode())

    # Sets the server username to what the server set it too
    global server_username
    server_username = connection_socket.recv(2048).decode()

    # Updates the window to show the new label
    clientFrame.update()

    # Calls function to send message to the server
    send_to_server(clientFrame, connection_socket)

def send_to_server(clientFrame, connection_socket):
    """ Displays an entry box that holds the message that will be sent to the server, activated with the click of the button

    Args:
        clientFrame (Frame): Frame in the window that displays content
        connection_socket (socket): Connection socket used to communicate with the server
    """
    global client_msg_entry

    # Creates a frame to enter information from the entry
    msg_entry_frame = Frame(clientFrame)
    msg_entry_frame.pack(padx=5, pady=5, side=TOP)

    # Creates a label widget the enter a message to send to the server
    client_msg_label = Label(msg_entry_frame, text='Enter a message to send to the server:')
    client_msg_label.pack(padx=5, pady=5, side=TOP)

    # Creates an entry widget for the client message
    client_msg_entry = Entry(msg_entry_frame)
    client_msg_entry.pack(padx=5, side=LEFT)

    # Creates a button that when clicked starts the on_ok_msg button function
    okBtn = Button(msg_entry_frame, text='OK', bd=3, command=lambda: on_ok_msg(msg_entry_frame, connection_socket))
    okBtn.pack(padx=5, side=LEFT)

def on_ok_msg(msg_frame, connection_socket):
    """ Gets the message and deletes the input label and output entry and sends the message to the server

    Args:
        msg_frame (Frame): Frame in the window that displays content
        connection_socket (socket): Connection socket used to communicate with the client
    """

    # Gets a message from the window
    send_client_message = client_msg_entry.get().strip()

    # Checks to see if the received message is empty and if so, displays a popup window
    if send_client_message == '':
        uiGen.show_popup("Invalid Input!")
    # Checks to see if the received message is end and if so, begins ending of the chat
    if send_client_message.lower() == 'end':
        uiGen.self_end_server(msg_frame, connection_socket, client_username)

    # Sets the server message to the input from the entry with the client username and time added on
    client_message = "<" + time.asctime(time.localtime()) + "> " + "[" + client_username + "]: " + send_client_message

    # Clears the current frame
    uiGen.clear_frame(msg_frame)

    # Creates a label to display the inputted client message to the window
    client_message_label = Label(msg_frame, text=client_message)
    client_message_label.pack(padx=5, pady=5)

    # Sends the client message to the server
    connection_socket.send(send_client_message.encode())

    # Starts the function to begin receiving from the server script
    receive_server(msg_frame, connection_socket)

def receive_server(clientFrame, connection_socket):
    """ Receives a message from the server and prints it to the window

    Args:
        clientFrame (Frame): Frame in the window that displays content
        connection_socket (socket): Connection socket used to communicate with the server
    """
    
    # Creates a frame to put the server information into
    connect_frame = Frame(clientFrame)
    connect_frame.pack(padx=5, pady=5, side=TOP)

    # Creates a label that displays a message
    connect_label = Label(connect_frame, text='Waiting for server to send a message...')
    connect_label.pack(padx=5, pady=5)

    # Updates the window to show the new label
    connect_frame.update()

    # Message received from the server
    server_message = connection_socket.recv(2048).decode()

    # If the server inputs end then begins ending the chat
    if server_message.lower() == "end":
        uiGen.other_end_client(connect_frame, connection_socket, server_username)

    # Modified server message to include the server username and time
    server_message = "<" + time.asctime(time.localtime()) + "> " + "[" + server_username + "]: " + server_message

    # Destroys previous label to allow for new label
    connect_label.destroy()

    # Creates a new label that displays the server message
    server_message_label = Label(connect_frame, text=server_message)
    server_message_label.pack(padx=5, pady=5)

    # Starts the function to start the sending process to the server
    send_to_server(connect_frame, connection_socket)
