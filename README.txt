# Python Chat Application

## Description

This project has a client and a server script that initializes a TCP connection to a server.

Client Script:
The client script asks the user for a valid IP address to connect to that server and the user can hit enter to set the default to localhost.
The script then checks if the inputted IP address is a valid using regular expression checking.
The script then asks the user for a valid port and the user can hit enter to set the port to default(8000).
The script then asks the user for a username and the user can hit enter to set the username to default(user).
The script then tries to connect to the server script and times out if the connection cannot be found.
Once the connection is initialized the user inputs a message to send to the server.
If the message is just whitespace then the user is told that it was invalid input and will have to re-enter a new message.
The user will continue to be asked to enter a new message until the message is valid.
If the user inputs a valid input but the input is end the program will end.
If the input is valid input and not end the clients username and message will be sent to the server.
After a while the server will send its username and message to the client.
The client will print the message to the screen or end the script if the server typed "end."

Server Script:
The server script asks the user for a valid IP address to connect to that server and the user can hit enter to set the default to localhost.
The script then checks if the inputted IP address is a valid using regular expression checking.
The script then asks the user for a valid port and the user can hit enter to set the port to default(8000).
The script then asks the user for a username and the user can hit enter to set the username to default(server).
The script then waits for the client script to connect.
Once the connection is made, the client script send a message over which is printed to the screen.
If the client script message is end then the script ends.
The server script is prompted to enter a message to send to the client.
The message is sent to the client unless the message is "end" then the script stops running.

I built this project to get more familiar with the python socket library and test sending information back and forth between a server and client.
I learned more about regular expressions and gained experience with the socket library while improving my ability to search for bugs

## Installation

1) Download a Python IDE of your choice
2) Open files inside of Python IDE
3) Run the server script and enter information up until "Trying to connect to another user..."
4) Run the client script

## Usage

1) Start the chatApplication_Server.py file and input the responses until it tries to connect with another user
    Output:
        Enter the server IP address (<Enter> for localhost):
        Enter the server port number (<Enter> for localhost):
        Enter your username (<Enter> for server):
        Trying to connect to another user...

2) Start the chatApplication_Client.py file
    Output:
        Enter the server IP address (<Enter> for localhost):
        Enter the server port number (<Enter> for localhost):
        Enter your username (<Enter> for user):
        Trying to connect to server....
        Connection established.
3) Type a message to send to the server
    Output:
        Enter a message to send to the server (Type end to stop): hello
        <Mon Apr 17 11:42:43 2023> [user]: hello

4) The server will receive the message from the client, type a message and send it back
    Output:
        Connection established.
        <Mon Apr 17 11:42:43 2023> [user]: hello
        Enter a message to send to the client (Type end to stop): hello
        <Mon Apr 17 11:42:58 2023> [server]: hello

5) The client will receive the message from the server, type a message and send it back
    Output:
        <Mon Apr 17 11:42:58 2023> [server]: hello
        Enter a message to send to the server (Type end to stop): end

6) Message back-and-fourth until one user enters end
    Output:
        Enter a message to send to the client (Type end to stop): end
        User server left the chat.
        Shutting down connection...