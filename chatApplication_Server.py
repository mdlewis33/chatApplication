from socket import *
import time
import re
from tkinter import *
import chatApplication_UI_Gen as uiGen

def server_setup(serverFrame):
    global server_port_entry
    global server_user_entry
    global server_ip_entry

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

    # Keeps the server frame alive until later destroyed/cleared
    serverFrame.mainloop()

def on_ok(serverFrame):
    # Regular expression statement to test
    regex = "^([0-9]{1,3}\.)([0-9]{1,3}\.){2}([0-9]{1,3})$"

    # Gets the inputted server ip from the server_ip_entry entry box
    server_ip = server_ip_entry.get()

    # Checks the server ip to see if it's empty, if so sets it to the default ip address (127.0.0.1)
    if server_ip == '':
        server_ip = '127.0.0.1'
    # Checks if the ip address matches the regular expression, if not creates a popup saying the ip was invalid
    if re.search(regex, server_ip):
        # uiGen.display_txt(serverFrame, server_ip)
    else:
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

    init_server_connect(serverFrame, server_ip, server_port)


def init_server_connect(serverFrame, server_ip, server_port):
    uiGen.clear_frame(serverFrame)

    # Create server socket
    server_socket = socket(AF_INET, SOCK_STREAM)

    # Bind server socket to ip and port
    server_socket.bind((server_ip, int(server_port)))

    # Listen for incoming connections
    server_socket.listen()

    connect_label = Label(serverFrame, text='Trying to connect to another user...')
    connect_label.pack(padx=5, pady=5)

    serverFrame.update()

    # Create connection socket
    connection_socket, address = server_socket.accept()

    # Receive the client message
    client_message = connection_socket.recv(2048).decode()

    connect_label.config(text='Connection established.')

    message_label = Label(serverFrame, text=f'Received message: {client_message}')
    message_label.pack(padx=5, pady=5)

    serverFrame.update()

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
