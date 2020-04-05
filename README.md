# Bman boilerplate
This is code that is useful for starting new BMAN Rcon scripting. Clone this repository and use it as a library for developing your own scripts.

It uses python3.8, requiring no outside libraries

RCON = Remote Console, its a way of getting information from BMan servers, and also sending commands. The full list of the types of information (events) is [here](https://github.com/Spasman/rcon_example)

Connecting to the Remote Console is done with [sockets](https://docs.python.org/3/library/socket.html)

## Settings values

First thing most people do when they want to run a script is to set up the settings file(`parseconfigs.py)`. This boilerplate was designed with connecting to multiple servers with the same rcon password in mind. Feel free to tweak with changes. The default values were chosen from the settings in a default installation of BM2.0 (as of beta 9), these assume that you are hosting a server on your own machine.

| Field  | Default   |  Description |
| ------------ | ------------ | -----|
|  `ip` | `127.0.0.1`  | The ip of the server you are connecting to|
|  `gamemode_socket` | `{'dm' : 42070}`  | The mapping of the gamemode name to its rconport|
|  `password` | admin  | default password is "admin" |
|  `blocking` | `false`  | Whether the processing continues if there is no packets incoming. best to keep this false for `set_timeout` to work|

Next step is creating a list of functions that handle different server events. A helpful list of these events are on [Spasmans Github](https://github.com/Spasman/rcon_example). In the repository I created a file `exampleapp.py` that contains the typical workflow of developing a handler:

```python
# import the enum type for rcon events
from rcontypes import rcon_event
# import json parsing to translate server messages into JSON type
import json

#this is the function that gets called each time sock receives a packet.
# event_id: the type of packet that is received for example "chat_message" or "player_death"
# message_string: information associated with that event
# sock: socket of the server. Use this for sending a command to the server on event
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
...
# start all the threads
for thread in threaddict:
    thread.start()
```

Now everything is set. Start the server with
`python startprocessing.py`
## Player Dictionary
If for whatever reason, you want to translate playerIDs into playerProfiles (think steam, gamejolt etc), you can use the cache option. Simply import `get_player_cache` from `update_cache`. And then calling `get_player_cache(player_dict)` returns a function that can be put into the function list for making sure the playerid -> player information is always consistent. This is useful for any scripts you want to write that need to store information tied to that user, for example: a player score, or any player specific information that needs to be persisted. You would need to event handlers in `update_cache.py`

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
- Server is not portforwarded

## Additional Server Commands (You can send these packets via rcon) besides the request data ones

In addition to the server commands for requesting data from the server, you can also use the following commands to mod the game. Many of them require mutators, so send: `enablemutators` before using them!

| Server command  | Description  |
| ------------ | ------------ |
| aimode  | Set certain AI behavior for all bots, NPCs, etc. Ai Mode ID 0 is normal behavior, AI mode ID 1 will deactivate their AI, AI mode 2 does nothing for now. Ai mode 3 will follow the path the host sets by middle clicking their mouse. I might add more later. [Requires mutators]  |
|  addtime "Seconds" | Adds time to the match clock. Must be 1 or more seconds.  |
| addbot "TeamID" "Difficulty"  |  Adds a bot to the specified team. 0 is deathmatch, 1 is USC, 2 is The Man. You can optionally specify their difficulty. |
| ban "PlayerName" "Reason  | Ban a specified player from your server so they can't rejoin and optionally give a reason why.  |
| cleartempbans  | Clear all temporary player bans.  |
| cure "PlayerName'  | Cure a specified player of all poison. [Requires Mutators]  |
| changeteam "PlayerName" "TeamID" |  Set a player to a specified team ID. 0 is deathmatch, 1 is USC, 2 is The Man, 3 is spectator.  |
|  changemap "MapFolder" | Ends the match and changes the map to the specified map folder. Use the full file path (Ex. maps\\stock\\fields)  |
| confetti "PlayerName"  |  Shows the confetti level up effect to the specified player. Leave PlayerName blank to show it to all players.  |
| clearchat  |   Clears the chat window of all text messages, similar to using \/clear in chat. |
| clear_rcon | Disconnects all existing RCON connections to the server. |
| currentwave | Displays the current wave if server is on Survival mode. |
| cmdlist "FileName" | Runs a list of commands from a text file, found in the 'cmdlist' folder in your AppData folder. Run the cmdlist 'example' to see an example. Command lists can enable mutators and have admin access, so be careful. |
| comictext "Text" "X" "Y" "Color1" "Color2" "Size" | Creates a comic text effect for all players, like when you fire a weapon. Provide the flavor text and the X and Y coordinates where the effect should appear. You can optionally set 2 colors for a gradient and the text size. Size can be 1-10, smallest to biggest. Hex colors should start with the character '#'. |
| drunk "PlayerName"  | Applies the drunk effect to the specified player. Leave PlayerName blank to make all players drunk. [Requires Mutators]  |
| deletesave "ProfileID" | Deletes any Survival saves stores on the server using the stored profile ID (Steam, GameJolt, etc). All Survival saves are wiped automatically on map change. |
| displayinfo | Outputs display resolution & display device debug information. |
|  endmatch | Ends the match and announces a winner.  |
| eventtext "Message" "Color"  | Displays a game event text with the given string and GML color to all players.  |
| enablemutators   | Enables mutators and allows you to use cheat commands. Disables earning achievements and some instances of getting XP for all players. You will need to restart the server if you want to turn it off.  |
|  echo "Message" "Color" |  Writes a message to the console log, with the specified Message string and GML color.  |
| explode "X" "Y" |  Detonates a normal explosion at the provided map coordinates. Does 100 damage. [Requires Mutators] |
| explodebig "X" "Y" | Detonates a big explosion at the provided map coordinates. Does 200 damage. [Requires Mutators] |
| forceweap "PlayerName" "Weap1" "Weap2" "Weap3" "Dual"  |   Force a loadout onto a specified player using weapon IDs and booleans. [Requires Mutators] |
|  flash "PlayerName' | Flashbang a specified player.  |
| globalsound "SoundName" | Used to play any in-game sound globally to all players on the server. Use the command 'listsfx' to generate a text file that lists the names of every in-game sound. [Requires Mutators] |
| help "Command"  | Shows description on a specified command.  |
|  kickbots |   Instantly kick all player bots from your server. |
|  kick "PlayerName" "Reason"   |   Kick a specified player from your server and optionally give a reason why.    |
| kill "PlayerName" "DeathType"    |   Kill a specified player and optionally give them a specified death animation ID. I'm not listing them all, figure it out yourself.   |
|   killenemies  |  Kill all currently alive NPCS (Survival enemies, zombie bots, map NPCs). [Requires Mutators]  |
|  killall   |  Kill all currently alive players.    |
|  killteam "TeamID"   |   Kill all currently alive players on the specified team ID. 0 is deathmatch, 1 is USC, 2 is The Man, 3 is spectator.   |
| listdir | Displays the 3 file directories Boring Man uses on your computer. |
| localsound "SoundName" "X" "Y" "Silenced" | Used to play any in-game sound at a position in the map. Provide the map position with 'X' and 'Y', set 'Silenced' to '0' or '1' to toggle whether the sound can be heard from far away or not. Use the command 'listsfx' to generate a text file that lists the names of every in-game sound. [Requires Mutators] |
| listsfx | Generates a text file that lists the name of every in-game sound. |
|  move "PlayerName" "X" "Y"   |    Move a specified player to the X and Y coordinates on the map. [Requires Mutators]   |
|  money "PlayerName" "MoneyAmount"   | Set an amount of money on a specified player. [Requires Mutators]     |
| matchtime | Displays the amount of time that has passed since last map change. |
| memoryuse | Displays the amount of memory the game is currently using. Windows only. |
| networkinfo    |   Displays network usage info.    |
|  objreport   |  Generates a text file report showing object, buffer and data structure amounts, saved at obj_report.txt in the AppData folder    |
| pm "PlayerName" "Message" "Color"    |   Send a server message to a specified player that only they will see. You can optionally set the GML color of the message too.    |
|  powerup "PlayerName" "PowerUpID"   |  Give a specified player a specified power up. 1 = triple damage, 2 = super speed, 3 = regen, 4 = invis, 5 = bfg [Requires Mutators]    |
|    pause |   Pause the match and make all players wait. Enter again to unpause.   |
| poison "PlayerName"    |  Poison a specified player to 100% poison. [Requires Mutators]    |
| playerinfo "PlayerName" | Get debug information for a connected player. Can use player name or player ID. |
|   rawsay  "Message" "Color"  |    Send a chat message as a server admin, without your name included. You can optionally set the GML color of the message too.  |
|   randbkgd  |   Randomizes the background color gradiant and overlay (client-side)   |
|  resetvicesall   |    Reset all the vices on all players to 0. [Requires Mutators]   |
| resetvicesplayer "PlayerName"   |   Reset all the vices on specified players to 0. [Requires Mutators]   |
| restartmap     |    Ends the match and restarts the server on the same map.  |
|  restartround   | Restarts the round in Team Deathmatch.     |
|   rcon "String"  |   Send a 'request_data' message to all rcon servers with the attached string.    |
| rconget "InstanceID" "CaseID" "RequestID" "PlayerID"    |   A command for RCON scripting. Not really for human use.   |
| revive "PlayerName" | Revives the specified player in Survival or Zombrains, free of charge. [Requires Mutators] |
| reviveall | Revives all players in Survival or Zombrains, free of charge. [Requires Mutators] |
| resetworld | Cleans up gameplay objects such as projectiles and weapon drops. [Requires Mutators] |
| resetplayer "PlayerName" | Resets the weapons, ammo and health on the specified player, as if they just respawned. [Requires Mutators] |
| resetallplayers | Performs the 'resetplayer' command on all players. [Requires Mutators] |
|   say "Message"  |   Send a chat message as a server admin.   |
| showcollision "0/1"  | Show collision objects that are normally invisible. They will display behind the tiles.  |
| showtiles "0/1"  |  Show or hide tiles. Recommended to hide tiles if you want to see the collision objects. |
| showpath "0/1"  | Show the AI paths of all AI characters and the last thing they waypointed to out of combat.   |
| setwave "WaveNumber" |  Skip to a certain wave number for Survival mode. [Requires Mutators] |
| setvice "PlayerName" "ViceID" "Amount"  | Set the amount of vices via vice ID on a specified player. [Requires Mutators]  |
| spawnenemy "EnemyID" "RankID" "Amount" | Spawn a Survival or Zombrains enemy. The rank determines their sub-type strength (Strong, Elite, etc). You can also optionally set an X and Y position for the enemy's spawn position, instead of using a spawn point. [Requires Mutators]  |
| setlife "PlayerName" "Amount"  |  Set the current health of a specified player. Maximum allowed is 200% of their maximum health.  |
| shock "PlayerName" | Shock\/stun a specified player. [Requires Mutators] |
| showlogic "0/1" | Shows logic gate lines and highlights interactable logic objects.  |
| skip | Skips waiting periods for Zombrains and Survival. |
| showhitbox "0/1" | Displays the hitboxes for various things. |
| stopcmdlist | Kills the command list, if one is running. |
| spawnbody "X" "Y" "Color" "Hat" "DeathType" | Spawns a dead body at the provided map coordinates. You also optionally specify the color of the dead body, what hat it wears and a specific death animation ID. Dead body physics aren't synchronized across the server except for the initial spawn, and not every player has ragdolls enabled so be wary of that. Hex colors should start with the character '#'. |
| shootingrange "0/1" | If a map is like the shooting range, setting this to '1' will enable extra time trial features and hud elements as if it were the stock shooting range. Resets to '0' on map change. [Requires Mutators] |
| showdps "0/1" | This will enable the HUD element showing your DPS (Damage Per Second). Only damage dealt against wooden target objects is measured for now. Resets to '0' on map change. |
| setrangetargets "InputObjectName" | This sets which type of object the shooting range HUD should keep track of when the time trial has started. It will only count individual, unique instances of the object that are using the logic gate system (outputting a signal). You can disable to HUD element again by setting this to '-1'. 'InputObjectName' should list suggestions for compatible ASSET objects from the map editor. Resets on map change. [Requires Mutators] |
| test "Test1" "Test2" | HELP (test): For testing console commands.  |
| tempban "PlayerName" "Reason" Minutes" |  Temporarily ban a player for X amount of minutes. Temp bans are removed on server restart. |
| unbanlast |  Unban the last player you banned using the 'ban' command.  |
| unpause | Unpause the match if its currently paused. |
| uptime  | Displays the current up time for the server. Does not reset if internet connection is lost.  |
| zombending | Triggers the Zombrains helicopter escape, if the setting is enabled. [Requires Mutators] |
