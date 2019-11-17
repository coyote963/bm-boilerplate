from enum import Enum

#Initialize enum. These are the same enums B-Man uses. this may be updated as the game is developed
#these enums identify game events, such as a flag being captured in CTF or a round ending in TDM
#For more information: https://github.com/Spasman/rcon_example
class rcon_event(Enum):
	server_startup = 0
	server_shutdown = 1
	lobby_connect = 2
	lobby_disconnect = 3
	player_connect = 4
	player_spawn = 5
	player_death = 6
	player_disconnect = 7
	player_team_change = 8
	player_level_up = 9
	player_get_powerup = 10
	player_damage = 11
	player_loaded = 12
	tdm_round_start = 13
	tdm_round_end = 14
	tdm_flag_unlocked = 15
	tdm_switch_sides = 16
	ctf_taken = 17
	ctf_dropped = 18
	ctf_returned = 19
	ctf_scored = 20
	ctf_generator_repaired = 21
	ctf_generator_destroyed = 22
	ctf_turret_repaired = 23
	ctf_turret_destroyed = 24
	ctf_resupply_repaired = 25
	ctf_resupply_destroyed = 26
	match_end = 27
	match_overtime = 28
	match_start = 29
	survival_new_wave = 30
	survival_flag_unlocked = 31
	survival_buy_chest = 32
	log_message = 33
	request_data = 34
	command_entered = 35
	rcon_logged_in = 36
	match_paused = 37
	match_unpaused = 38
	warmup_start = 39
	rcon_disconnect = 40
	rcon_ping = 41
	chat_message = 42
	survival_get_vice = 43
	survival_use_vice = 44
	survival_player_revive = 45
	player_taunt = 46
	survival_complete_mission = 47
	survival_take_mission = 48
	survival_fail_mission = 49

#use these enums when sending requests to your server so the server knows what to do with them
class rcon_receive(Enum):
	login = 0
	ping = 1
	command = 2
	request_player = 3
	request_bounce = 4
	request_match = 5
	confirm = 6
	request_scoreboard = 7
