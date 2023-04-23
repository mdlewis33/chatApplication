from socket import *
import time
import re
from tkinter import *
import chatApplication_UI_Gen as uiGen

def client_setup(clientFrame):
    global client_port_entry
    global client_user_entry
    global client_ip_entry

    uiGen.clear_frame(clientFrame)

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

    client_user_entry = Entry(user_entry_frame)
    client_user_entry.pack(side=LEFT)

    okBtn = Button(clientFrame, text='OK', command=lambda: on_ok(clientFrame))
    okBtn.pack(side=TOP)

def on_ok(clientFrame):
    global client_ip
    global client_port
    global client_username

    # Regular expression statement
    regex = "^([0-9]{1,3}\.)([0-9]{1,3}\.){2}([0-9]{1,3})$"

    client_ip = client_ip_entry.get().strip()

    if client_ip == '':
        client_ip = '127.0.0.1'
    if not re.search(regex, client_ip):
        uiGen.show_popup("Invalid IP Address.")

    client_port = client_port_entry.get().strip()

    if client_port == '':
        client_port = 8000

    client_username = client_user_entry.get().strip()

    if client_username == '':
        client_username = 'user'

    init_client_connect(clientFrame)

def init_client_port():
    # Set the client port number
    global client_port
    client_port = input("Enter the server port number (<Enter> for localhost): ")
    if client_port == '':
        client_port = 8000
    init_client_username()

def init_client_username():
    # Set the client username
    global client_username
    client_username = input("Enter your username (<Enter> for user): ")
    if client_username == '':
        client_username = 'user'
    init_client_connect()

def init_client_connect(clientFrame):
    uiGen.clear_frame(clientFrame)

    connection_socket = socket(AF_INET, SOCK_STREAM)

    connection_socket.settimeout(5)

    connect_label = Label(clientFrame, text='Trying to connect to server...')
    connect_label.pack(padx=5, pady=5)

    clientFrame.update()

    try:
        connection_socket.connect((client_ip, int(client_port)))
    except socket.error:
        uiGen.show_popup("Server IP or port is incorrect.")
        client_setup(clientFrame)

    connection_socket.settimeout(None)

    time.sleep(1)

    connect_label.config(text='Connection established.')

    connection_socket.send(client_username.encode())

    global server_username
    server_username = connection_socket.recv(2048).decode()

    clientFrame.update()

    send_to_server(clientFrame, connection_socket)

def send_to_server(clientFrame, connection_socket):
    global client_msg_entry

    msg_entry_frame = Frame(clientFrame)
    msg_entry_frame.pack(padx=5, pady=5, side=TOP)

    client_msg_label = Label(msg_entry_frame, text='Enter a message to send to the server:')
    client_msg_label.pack(padx=5, pady=5, side=TOP)

    client_msg_entry = Entry(msg_entry_frame)
    client_msg_entry.pack(padx=5, side=LEFT)

    okBtn = Button(msg_entry_frame, text='OK', bd=3, command=lambda: on_ok_msg(msg_entry_frame, connection_socket))
    okBtn.pack(padx=5, side=LEFT)

def on_ok_msg(msg_frame, connection_socket):

    send_client_message = client_msg_entry.get().strip()

    if send_client_message == '':
        uiGen.show_popup("Invalid Input!")
    if send_client_message.lower() == 'end':
        client_end_client(msg_frame, connection_socket)

    # Sets the server message to the input from the entry with the server username and time added on
    client_message = "<" + time.asctime(time.localtime()) + "> " + "[" + client_username + "]: " + send_client_message

    # Clears the current frame
    uiGen.clear_frame(msg_frame)

    client_message_label = Label(msg_frame, text=client_message)
    client_message_label.pack(padx=5, pady=5)

    connection_socket.send(send_client_message.encode())

    receive_server(msg_frame, connection_socket)

def receive_server(clientFrame, connection_socket):
    connect_frame = Frame(clientFrame)
    connect_frame.pack(padx=5, pady=5, side=TOP)

    # Creates a label that displays a message
    connect_label = Label(connect_frame, text='Waiting for server to send a message...')
    connect_label.pack(padx=5, pady=5)

    # Updates the window to show the new label
    connect_frame.update()

    server_message = connection_socket.recv(2048).decode()

    if server_message.lower() == "end":
        client_end_server(connect_frame, connection_socket)

    server_message = "<" + time.asctime(time.localtime()) + "> " + "[" + server_username + "]: " + server_message

    connect_label.destroy()

    server_message_label = Label(connect_frame, text=server_message)
    server_message_label.pack(padx=5, pady=5)

    send_to_server(connect_frame, connection_socket)

def client_end_client(clientFrame, connection_socket):

    uiGen.clear_frame(clientFrame)

    leave_msg = Label(clientFrame, text="[" + client_username + "]" + " left the chat")
    leave_msg.pack(padx=4, pady=5)

    closing_msg = Label(clientFrame, text="Shutting down connection...")
    closing_msg.pack(padx=5, pady=5)

    clientFrame.update()

    connection_socket.send("end".encode())

    connection_socket.close()

    time.sleep(5)

    clientFrame.winfo_toplevel().destroy()

def client_end_server(clientFrame, connection_socket):

    uiGen.clear_frame(clientFrame)

    leave_msg = Label(clientFrame, text="[" + server_username + "]" + " left the chat")
    leave_msg.pack(padx=4, pady=5)

    closing_msg = Label(clientFrame, text="Shutting down connection...")
    closing_msg.pack(padx=5, pady=5)

    # Update the window to display the new labels
    clientFrame.update()

    connection_socket.close()

    time.sleep(5)

    clientFrame.winfo_toplevel().destroy()
