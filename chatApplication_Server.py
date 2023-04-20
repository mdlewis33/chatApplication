from socket import *
import time
import re
from tkinter import *
import chatApplication_UI_Gen as uiGen

def server_setup(serverFrame):
    global server_port_entry
    global server_user_entry
    global server_ip_entry

    # Create a label and an entry widget for the server IP address
    server_ip_label = Label(serverFrame, text='Enter the server IP address (Leave blank for localhost):')
    server_ip_label.pack(padx=5, pady=5, side=TOP)

    ip_entry_frame = Frame(serverFrame)
    ip_entry_frame.pack(padx=5, pady=5, side=TOP)

    server_ip_entry = Entry(ip_entry_frame)
    server_ip_entry.pack(side=LEFT)


    server_port_label = Label(serverFrame, text='Enter the server port number (Leave blank for localhost): ')
    server_port_label.pack(padx=5, pady=5, side=TOP)

    port_entry_frame = Frame(serverFrame)
    port_entry_frame.pack(padx=5, pady=5, side=TOP)

    server_port_entry = Entry(port_entry_frame)
    server_port_entry.pack(side=LEFT)


    server_user_label = Label(serverFrame, text='Enter your username (Leave blank for server): ')
    server_user_label.pack(padx=5, pady=5, side=TOP)

    user_entry_frame = Frame(serverFrame)
    user_entry_frame.pack(padx=5, pady=5, side=TOP)

    server_user_entry = Entry(user_entry_frame)
    server_user_entry.pack(side=LEFT)

    okBtn = Button(serverFrame, text='OK', bd=3, command=lambda: on_ok(serverFrame))
    okBtn.pack(side=BOTTOM)

    serverFrame.mainloop()

def on_ok(serverFrame):
    # Regular expression statement
    regex = "^([0-9]{1,3}\.)([0-9]{1,3}\.){2}([0-9]{1,3})$"

    global server_ip
    server_ip = server_ip_entry.get()
    if server_ip == '':
        server_ip = '127.0.0.1'
    if re.search(regex, server_ip):
        uiGen.display_txt(serverFrame, server_ip)
    else:
        uiGen.show_popup("Invalid IP Address.")

    global server_port
    server_port = server_port_entry.get()
    if server_port == '':
        server_port = 8000
    uiGen.display_txt(serverFrame, server_port)

    global server_username
    server_username = server_user_entry.get()
    if server_username == '':
        server_username = 'server'
    uiGen.display_txt(serverFrame, server_username)

    #get_setup(serverFrame)

def get_setup(serverFrame):
    uiGen.clear_frame(serverFrame)



def init_server_connect():
    # Create server socket
    server_socket = socket(AF_INET, SOCK_STREAM)

    # Bind server socket to ip and port
    server_socket.bind((server_ip, int(server_port)))

    # Listen for incoming connections
    server_socket.listen()

    print("Trying to connect to another user...")

    # Create connection socket
    connection_socket, address = server_socket.accept()

    # Receive the client message
    client_message = connection_socket.recv(2048).decode()

    print("Connection established.")

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
