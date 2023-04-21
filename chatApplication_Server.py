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
    okBtn.pack(side=BOTTOM)

# Gets the answers entered into the entry's and save them into variables.
# serverFrame = Frame in the window that displays content
def on_ok(serverFrame):
    global server_ip
    global server_port
    global server_username

    # Regular expression statement to test
    regex = "^([0-9]{1,3}\.)([0-9]{1,3}\.){2}([0-9]{1,3})$"

    # Gets the inputted server ip from the server_ip_entry entry box
    server_ip = server_ip_entry.get()

    # Checks the server ip to see if it's empty, if so sets it to the default ip address (127.0.0.1)
    if server_ip == '':
        server_ip = '127.0.0.1'
    # Checks if the ip address matches the regular expression, if not creates a popup saying the ip was invalid
    if not re.search(regex, server_ip):
        # uiGen.display_txt(serverFrame, server_ip)
        uiGen.show_popup("Invalid IP Address.")

    # Gets the inputted server port from the server_port_entry entry box
    server_port = server_port_entry.get()

    # Checks if the server port is empty, if so sets it to the default port number (8000)
    if server_port == '':
        server_port = 8000
    #uiGen.display_txt(serverFrame, server_port)

    # Gets the inputted server username from the server_user_entry
    server_username = server_user_entry.get()

    # Checks if the server username is empty, if so sets it to the default server username (server)
    if server_username == '':
        server_username = 'server'
    uiGen.display_txt(serverFrame, server_username)

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
    connect_label = Label(serverFrame, text='Waiting for client to send a message...')
    connect_label.pack(padx=5, pady=5)

    serverFrame.update()

    client_message = connection_socket.recv(2048).decode()

    client_message = "<" + time.asctime(time.localtime()) + "> " + "[" + client_username + "]: " + client_message

    connect_label.destroy()

    client_message_label = Label(serverFrame, text=client_message)
    client_message_label.pack(padx=5, pady=5)

    send_to_client(serverFrame, connection_socket)

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

def on_ok_msg(frame, connection_socket):

    send_server_message = server_msg_entry.get()
    server_message = "<" + time.asctime(time.localtime()) + "> " + "[" + server_username + "]: " + send_server_message

    uiGen.clear_frame(frame)

    server_message_label = Label(frame, text=server_message)
    server_message_label.pack(padx=5, pady=5)

    connection_socket.send(send_server_message.encode())

    receive_client(frame, connection_socket)

def main_loop():
    # Loop that continues the chat between the server(this file) and the client until either inputs "end"
    while True:
        # Initializes server message for sending to client
        server_message = server_username + "."

        # Splits the received message from client into username and message
        client_username = client_message.split(".")[0]
        client_message = client_message.split(".")[1]

        # Checks to see if the received message is end and if so, exits the loop
        if client_message.lower() == "end":
            break

        # Displays the clients username and message to the screen
        print("<" + time.asctime(time.localtime()) + "> " + "[" + client_username + "]: " + client_message)

        # Receives the servers message
        server_message_input = input("Enter a message to send to the client (Type end to stop): ").strip()

        # Checks if the inputted message is empty and if so, the server has to input until the message is not empty
        while server_message_input == "":
            print("Invalid Input.")
            server_message_input = input("Enter a message to send to the client (Type end to stop): ").strip()

        # Stops the loop if the user inputs end
        if server_message_input.lower() == "end":
            break

        # Adds the input message to the previously prepared message to send to client
        server_message = server_username + "." + server_message_input

        # Prints the servers username and inputted message to the screen
        print("<" + time.asctime(time.localtime()) + "> " + "[" + server_username + "]: " + server_message_input)

        # Sends the inputted message to the client
        connection_socket.send(server_message.encode())

        # Receive the client message
        client_message = connection_socket.recv(2048).decode()


def server_end():
    # When the loop ends checks if the client or server ended the chat and responds accordingly
    if client_message == "end":
        print(client_username + " left the chat.")
        print("Shutting down connection...")
    else:
        print(server_username + " left the chat.")
        print("Shutting down connection...")
        connection_socket.send((server_username + ".end").encode())

    # Closes the server socket
    connection_socket.close()
