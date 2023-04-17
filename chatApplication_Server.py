from socket import *
import time
import re

# Regular expression statement
regex = "^([0-9]{1,3}\.)([0-9]{1,3}\.){2}([0-9]{1,3})$"

# Set the server IP address and checks to see if the IP address is valid
valid = False
while not valid:
    server_ip = input("Enter the server IP address (<Enter> for localhost): ")
    if server_ip == '':
        server_ip = '127.0.0.1'

        if re.search(regex, server_ip):
            valid = True

# Set the server port number
server_port = input("Enter the server port number (<Enter> for localhost): ")
if server_port == '':
    server_port = 8000

# Set the server username
server_username = input("Enter your username (<Enter> for server): ")
if server_username == '':
    server_username = 'server'

#Create server socket
server_socket = socket(AF_INET, SOCK_STREAM)

#Bind server socket to ip and port
server_socket.bind((server_ip, int(server_port)))

#Listen for incoming connections
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

# When the loop ends checks if the client or server ended the chat and responds accordingly
if client_message == "end":
    print(client_username + " left the chat.")
    print("Shutting down connection...")
else:
    print(server_username + " left the chat.")
    print("Shutting down connection...")
    connection_socket.send((server_username + ".end").encode())

# Closes the server script
connection_socket.close()
