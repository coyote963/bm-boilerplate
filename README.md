# Bman boilerplate
This is code that is useful for starting new BMAN Rcon scripting. Clone this repository and use it as a library for developing your own scripts.

It uses python3.8, requiring no outside libraries

## Settings values

First thing most people do when they want to run a script is to set up the settings file(`parseconfigs.py`. This boilerplate was designed with connecting to multiple servers with the same rcon password in mind. Feel free to tweak with changes. The default values were chosen from the settings in a default installation of BM2.0 (as of beta 9)

| Field  | Default   |  Description |
| ------------ | ------------ | -----|
|  `ip` | 127.0.0.1  | The ip of the server you are connecting to|
|  `gamemode_socket` | `{'dm' : 42070}`  | The mapping of the gamemode name to its rconport|
|  `password` | admin  | d|
|  `blocking` | `false`  | Whether the processing continues if there is no packets incoming. best to keep this false for `set_timeout` to work|

Next step is creating a list of functions that handle different server events. A helpful list of these events are on [Spasmans Github](https://github.com/Spasman/rcon_example). In the repository I created a file `exampleapp.py` that contains the typical workflow of developing a handler:

```python
# import the enum type for rcon events
from rcontypes import rcon_event
# import json parsing to translate server messages into JSON type
import json

#optional: add in automatic table lookup for translating PlayerID's to Player Profile + Store
# from update_cache import get_handle_cache
# player dict for this scope only, useful for packets that only have playerId
# player_dict = {}
# handle_cache = get_handle_cache(player_dict)

#this is the function that gets called each time sock receives a packet.
def handle_chat(event_id, message_string, sock):
    # if passed in event_id is a chat_message, otherwise do nothing
    if event_id == rcon_event.chat_message.value:
        # parse the json
        js = json.loads(message_string)
        # if the server message is from a player
        if 'PlayerID' in js and js['PlayerID'] != '-1':
            # print it into console
            print("{} said {}".format(js['Name'],js['Message']))



example_functions  = [handle_chat] # include handle_cache if you are using it
```

This code needs to be included in the main execution loop. To do this, import the list of functions that are each called with the three parameters `event_id, message_string, sock`
into the file `startprocessing.py`. Executing `python startprocessing.py` will run all the code you defined.
```python
# import all the functions from the example
from exampleapp import example_functions
...
#start a thread with the list of functions imported from exampleapp
threaddict[mode] = threading.Thread(target = start_parser, args = (sock, get_execute_functionlist(example_functions)))
    
```

Now everything is set. Start the server with
`python startprocessing.py`
## Player Dictionary
If for whatever reason, you want to translate playerIDs into playerProfiles (think steam, gamejolt etc), you can use the cache option. Simply import `get_player_cache` from `update_cache`. And then calling `get_player_cache(player_dict)` returns a function that can be put into the function list for making sure the playerid -> player information is always consistent. This is useful for any scripts you want to write that need to store information tied to that user, for example: a player score, or any player specific information that needs to be persisted

## Expanding to more servers (advanced)
If you want to have more servers, here is the workflow
1. add an extra entry into gamemode_socket dict, with the key being the gamemode and the value being the port. For example:
`socket_dict = { 'dm' : 42070, 'svl': 42071 }`
2. add the additional functionality in a function. Put all the event handlers in a list and export that list
3. Import that list into `startprocessing.py` then add if statement for the new gamemode,
`threaddict[mode] = threading.Thread(target = start_parser, args = (sock, get_execute_functionlist(new_functions)))`


Common Issues:
- Rcon is not enabled on the target server
- Port selected is not the rcon port, but the game port
