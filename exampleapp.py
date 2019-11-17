# import the enum type for rcon events
from rcontypes import rcon_event
# import json parsing to translate server messages into JSON type
import json

#optional: add in automatic table lookup for translating PlayerID's to Player Profile + Store
# from update_cache import get_handle_cache
# player dict for this scope only, useful for packets that only have playerId
# player_dict = {}
# handle_cache = get_handle_cache(player_dict)

def handle_chat(event_id, message_string, sock):
    # if passed in event_id is a chat_message
    if event_id == rcon_event.chat_message.value:
        # parse the json
        js = json.loads(message_string)
        # if the server message is from a player
        if 'PlayerID' in js and js['PlayerID'] != '-1':
            # print it into console
            print("{} said {}".format(js['Name'],js['Message']))



example_functions  = [handle_chat] # include handle_cache if you are using it