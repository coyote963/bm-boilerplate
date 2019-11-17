import struct
import sys
import datetime
import json
import time
from rcontypes import rcon_event, rcon_receive
from helpers import send_packet, get_socket



#this function isn't used but its example code of parsing the 'PlayerData' JSON set
#It itorates through an entire JSON string looking for keys that start with the string 'PlayerData'
#If found, you can use the 'k' variable as an accessor for each key/value pair
#just look at the damn code, whatever, fuck
def scoreboard(jsonString):
	js = json.loads(jsonString)
	for k in js.items():
		if k.startswith("PlayerData"):
			name = js[k]['Name']
			kills = js[k]['Kills']
			deaths = js[k]['Deaths']
			assists = js[k]['Assists']
			print(str(name)+" - K: "+str(kills)+" D: "+str(deaths)+" A: "+str(assists))



def start_parser(sock, cb):
	#initialize some globals for network data reading
	#sock.recv() uses bytes so lets make them empty byte arrays
	buffer = b''
	get_data = b''
	data = b''

	#these two are the delimiters for B-Man packets
	start_read = b'\xe2\x94\x90' #translates to ascii character "┐"
	end_read = b'\xe2\x94\x94' #translates to ascii character "└"

	timeout = 0 #used for timing out a bad connection

	while True:
		timeout += 1
		if timeout > 3600000:
			#increase timeout value and if it reaches more then 3600000, kill the app
			#timeout is reset when rcon receives an "rcon_event.rcon_ping.value" event from the game server
			print("Timed out from server!")
			sys.exit()
		data = b'' #reset main data byte array
		try:
			#attempt to load bytes from the network
			#buffer size read per cycle set to 64k because YEET
			#set it to something lower if youre having network performance problems
			get_data = sock.recv(64000)
		except:
			get_data = b'' #return empty byte array is fail
		if get_data != b'':#if the byte array is not empty, load them into the current data buffer
			buffer += get_data
		while True: #a second while loop is needed to loop through the buffer to make sure all data is processed
			if buffer.find(end_read) != -1 and buffer.find(start_read) != -1: #this if-else statement checks if the data buffer has the beginning delimiter and the end delimiter
				start_index = buffer.find(start_read) #find the beginning byte position of the Boring Man packet
				end_index = buffer.find(end_read)+3 #find the ending byte position of the Boring Man packet and offset it to make sure its included (1 character string = 3 bytes)
				data = buffer[start_index:end_index] #carve out the complete packet out of the data buffer and assign it to the 'data' variable for processing
				buffer = buffer[end_index:] #take the complete packet out of the buffer so only the unused data is left so it can be used next cycle
				if data != b'': #make sure the data variable isn't empty
					data_info = struct.unpack_from('<'+'3s'+'h',data,0) #read the beginning delimiter character, and then the JSON string size (in bytes)
					event_data = struct.unpack_from('<'+'3s'+'h'+'h'+str(data_info[1])+'s',data,0) #read the beginning delimiter character, and then the JSON string size, then the event ID integer, then the JSON string itself using the size value from the line above
					data = b'' #reset the data variable 
					event_id = event_data[2] #get the event ID number
					message_string = event_data[3].decode().strip() #get the JSON string and sanitize it
					message_string = message_string[:-1] #remove the ending delimiter character (└)
					
					#uncomment the print line below to see the event IDs received and the JSON data that comes with them
					#print("EVENT ID: "+str(event_id)+" - JSON: "+str(message_string)) 
					#
					#!!BELOW IS WHERE YOU SHOULD START PROCESSING THE GAME'S JSON DATA!!
					#
					if event_id == rcon_event.rcon_ping.value: #if the event is a ping
						#event ID for pinging. Boring Man will send each RCON client a ping event every few seconds, reply to it to keep your connection alive
						#use the 'rcon_receive.ping' enum for pinging, this tells the server its just a ping packet and to do nothing with it
						timeout = 0 #reset timeout if a ping is received
						send_packet(sock, "1",rcon_receive.ping.value) #i put a "1" string cuz sometimes game maker gets mad at empty strings
					#
					#this event ID is for logging in-game console messages in your python window
					if event_id == rcon_event.log_message.value:
						js = json.loads(message_string)
						#print(js['Message']) #load the JSON key 'Message' to get the log message
					#
					#
					if event_id == rcon_event.server_shutdown.value:
						#end the app if it receives a "server_shutdown" event
						print("Server disconnected")
						sys.exit()
					
					cb(event_id, message_string, sock)
			else:
				break #break out of this while loop if the beginning or ending delimiter characters aren't found and go back to reading network data

