import threading
import json
from bm_parser import start_parser
from helpers import get_socket
from rcontypes import rcon_event, rcon_receive
from exampleapp import example_functions

def get_execute_functionlist(example_functions):
    def execute_functionlist(event_id, message_string, sock):
        for f in example_functions:
            f(event_id, message_string, sock)
    return execute_functionlist

if __name__ == "__main__":
    # add in additional gamemodes if hosting multiple servers
    gamemodes = ['svl']
    # this holds all the threads
    threaddict = {}
    for mode in gamemodes:
        sock = get_socket(mode)
        if mode == 'svl':
            threaddict[mode] = threading.Thread(target = start_parser, args = (sock, get_execute_functionlist(example_functions)))
    
    for mode, thread in threaddict.items():
        thread.start()

    for mode, thread in threaddict.items():
        thread.join()