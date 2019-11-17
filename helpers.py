import struct
import sys
import socket
from rcontypes import rcon_receive
from parseconfigs import ip, password, blocking, get_port

# function to get a socket object
def get_socket(gamemode):
	
	server_address = (ip, get_port(gamemode))
	server_password = password
	#attempt a connection to the Boring Man server, or crash if you can't
	#create a global TCP socket, Boring Man RCON uses a separate TCP socket unlike the rest of the games netcode
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	#we turn TCP blocking on and off because its just easier that way
	if not blocking:
		sock.setblocking(1)
		sock.connect(server_address)
		sock.setblocking(0)
	else:
		sock.connect(server_address)
	#send a 'rcon_receive.login' packet with your RCON password as the string data
	send_packet(sock, server_password,rcon_receive.login.value)
	return sock


#declaring a function for sending packets over socket to game maker networking
#the message contains a signed integer for the enum event ID, then a string with data to process on the server
def send_packet(sock, packetData,packetEnum):
	packet_message = packetData+"\00" #add a null terminating character at the end of your string because game maker is stupid
	packet_size = len(bytes(packet_message, 'utf-8')) #get the byte size of your string
	s = struct.Struct('h'+str(packet_size)+'s') #create a data structure with an int and a string (with the string size)
	packet = s.pack(packetEnum,packet_message.encode('utf-8')) #pack and encode your message for game maker usage
	sock.send(packet) #send that bitch


#send a packet with two arguments
#the message contains a signed integer for the enum event ID, then a string with data to process on the server, and a request ID
def send_request(sock, requestID, packetData, packetEnum):
	packet_message = '"' + requestID + '" "' + packetData + '"' 
	send_packet(sock, packet_message, packetEnum)
	