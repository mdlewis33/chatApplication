import subprocess

client_app = subprocess.Popen(['python', 'chatApplication_Client_Launch.py'])
server_app = subprocess.Popen(['python', 'chatApplication_Server_Launch.py'])

client_app.wait()
server_app.wait()