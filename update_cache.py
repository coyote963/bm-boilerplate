from rcontypes import rcon_event, rcon_receive
import json

def handle_scoreboard(event_id, message_string, player_dict):
    if event_id == rcon_event.request_data.value:
        js = json.loads(message_string)
        if int(js['CaseID']) == rcon_receive.request_scoreboard.value:
            for k in js.keys():
                if k.startswith('PlayerData') and js[k]['Bot'] != "1":
                    player_dict[js[k]['ID']] = {
                        'profile' : js[k]["Profile"],
                        'platform' : js[k]['Store']
                    }


def handle_join(event_id, message_string, player_dict):
    if event_id == rcon_event.player_connect.value:
        js = json.loads(message_string)
        x = json.loads(js['Profile'])
        player_dict[js['PlayerID']] = {
            'profile' : js["Profile"],
            'platform' : js['Store']
        }


cache_functions = [handle_scoreboard, handle_join]

def get_handle_cache(player_dict):
    def handle_cache(event_id, message_string, sock):
        for f in cache_functions:
            f(event_id, message_string, player_dict)
    return handle_cache

