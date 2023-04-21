import socket
import time
import re

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

def init_client_connect():
    # Create client socket using TCP
    global client_socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.settimeout(5)
    print("Trying to connect to server....")

    # Attempts to connect to the server, fails if wrong ip/port
    try:
        client_socket.connect((client_ip, int(client_port)))
    except socket.error:
        print("Server IP or port is incorrect.")
        exit(1)

    client_socket.settimeout(None)
    time.sleep(1)
    client_socket.send(client_username.encode())
    print("Connection established.")


    # Loop that continues the chat between the server and the client(this file) until either inputs "end"
    while True:
        # Initializes client message for sending to server
        client_message = ""

        # Get user message to send to the client
        client_message_input = input("Enter a message to send to the server (Type end to stop): ").strip()

        # Checks if the inputted message is empty and if so, the client has to input until the message is not empty
        while client_message_input == "":
            print("Invalid Input.")
            client_message_input = input("Enter a message to send to the server (Type end to stop): ").strip()

        # Stops the loop if the user inputs end
        if client_message_input.lower() == "end":
            break

        # Adds the input message to the previously prepared message to send to server
        client_message += client_message_input

        # Prints the inputted message to the screen
        #print("<" + time.asctime(time.localtime()) + "> " + "[" + client_username + "]: " + client_message_input)

        # Sends message to the server
        client_socket.send(client_message.encode())

        # Waits and receives new message from the server
        server_message = client_socket.recv(2048).decode()

        # Splits the inputted string into the username and received message
        #server_username = server_message.split(".")[0]
        #server_message = server_message.split(".")[1]

        # Checks to see if the received message was end and if so, ends the loop
        if server_message.lower() == "end":
            break

        # Prints the received message to the screen with the servers username
        print("<" + time.asctime(time.localtime()) + "> " + "[" + server_username + "]: " + server_message)

def client_end():
    # When the loop ends checks if the client or server ended the chat and responds accordingly
    if client_message_input == "end":
        print("User " + client_username + " left the chat.")
        print("Shutting down connection...")
        client_socket.send((client_username + ".end").encode())
    else:
        print("User " + server_username + " left the chat.")
        print("Shutting down connection...")

    # Closes the client socket
    client_socket.close()

# Regular expression statement
regex = "^([0-9]{1,3}\.)([0-9]{1,3}\.){2}([0-9]{1,3})$"

# Set the server IP address and checks to see if the IP address is valid
valid = False
while not valid:
    global client_ip
    client_ip = input("Enter the server IP address (<Enter> for localhost): ")
    if client_ip == '':
        client_ip = '127.0.0.1'
    if re.search(regex, client_ip):
            valid = True

init_client_port()
