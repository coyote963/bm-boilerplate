
# IP Address of the host
ip = '127.0.0.1'
# Gamemode to port mapping
gamemode_ports = {'svl' : 42070}

#server rcon password
password = 'admin'

# set to true for performance, set to false for reliability
blocking = True


#helper function to get the port given a gamemode
def get_port(gamemode):
    return gamemode_ports[gamemode]
