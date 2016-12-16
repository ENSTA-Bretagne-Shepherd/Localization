import socket
from shepherd_json_socket import *

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.bind(('', 15555))

while True:
	socket.listen(5)
	client, address = socket.accept()

	messagePosBateau = client.recv(255)
	messageCaptBouee = client.recv(255)
	localisation(messagePosBateau, messageCaptBouee)

print("Close")
socket.close()
