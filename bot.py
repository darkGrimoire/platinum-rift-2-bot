import sys
import math

import random
# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

# player_count: the amount of players (always 2)
# my_id: my player ID (0 or 1)
# zone_count: the amount of zones on the map
# link_count: the amount of links between all zones
player_count, my_id, zone_count, link_count = [int(i) for i in input().split()]
for i in range(zone_count):
	# zone_id: this zone's ID (between 0 and zoneCount-1)
	# platinum_source: Because of the fog, will always be 0
	zone_id, platinum_source = [int(j) for j in input().split()]

links1 = []		# array for linked zone
links2 = []
for i in range(link_count):									# sys
	zone_1, zone_2 = [int(j) for j in input().split()]		# sys
	links1.append(zone_1)									# collecting data of linked zone in links1 and links2
	links2.append(zone_2)									# zone with id links1[i] are connected to zone links2[i]

# VAR
if my_id == 0:
	enemy_id=1
else:
	enemy_id=0
enemyBase = -1
myBase = -1
zone_dist = [ float("inf") for i in range(zone_count) ]			# array of zone distance for dijkstra algorithm, the index is zone ID

# MOVEMENT_BASIC
def moves(x):							# input a zone ID and gives back the adjacent zone in an array
	aval = []
	for i in range(len(links1)):
		if x == links1[i]:
			aval.append(links2[i])
	for i in range(len(links2)):
		if x == links2[i]:
			aval.append(links1[i])
	return aval

# Dijkstra algorithm, mapping the shortest distance to all zones
def dijkstra(point):	
	avail_moves = moves(point)
	alg_done = True
	for i in range(len(moves(point))):
		if zone_dist[ avail_moves[i] ] > (zone_dist[point] + 1) :
			zone_dist[ avail_moves[i] ] = (zone_dist[point] + 1)
			alg_done = False
	if alg_done == False :
		for i in range (len(moves(point))):
			dijkstra(avail_moves[i])
# pathfinder algorithm, finding the zone path to a desired location, need to add eff_path codeblock after function used
def path_find(a, b) :
	if a != b :
		avail_moves = moves(b)
		for i in range(len(avail_moves)):
			if zone_dist[ avail_moves[i] ] == (zone_dist[b] - 1) and len(path) < max(zone_dist)+1 :
				path.append(avail_moves[i])
				path_find(a, avail_moves[i])

# game loop
while True:
	vis_zone = []
	pods = []
	pods_atk = []
	pods_def = []
	my_zone = []
	my_platinum = int(input())  # your available Platinum
	for i in range(zone_count):
		# z_id: this zone's ID
		# owner_id: the player who owns this zone (-1 otherwise)
		# pods_p0: player 0's PODs on this zone
		# pods_p1: player 1's PODs on this zone
		# visible: 1 if one of your units can see this tile, else 0
		# platinum: the amount of Platinum this zone can provide (0 if hidden by fog)
		z_id, owner_id, pods_p0, pods_p1, visible, platinum = [int(j) for j in input().split()]
		if visible:
			vis_zone.append(z_id)								# array of visible zone
			if enemyBase == -1 and owner_id == enemy_id:		# sets the enemyBase zone ID
				enemyBase = z_id	
			if myBase == -1 and owner_id == my_id:				# sets myBase zone ID, works same like enemyBase
				myBase = z_id									# the (enemyBase == -1) part makes this only true at game beginning, when enemyBase=-1 (see #VAR)
			if owner_id == my_id:
				my_zone.append(z_id)							# array of zone owned
		if my_id == 0:
			if pods_p0 > 0:
				pods.append([z_id, pods_p0, pods_p1])				# array of pods located: [location, number of pods: player 0(me), player 1]
		else:
			if pods_p1 > 0:
				pods.append([z_id, pods_p1, pods_p0])				# array of pods located: [location, number of pods: player 1(me), player 0]

	# Write an action using print
	# To debug: print("Debug messages...", file=sys.stderr)
	
	# Pathfinding algorithm
	zone_dist[myBase] = 0
	dijkstra(myBase)
	path = [enemyBase]
	path_find(myBase, enemyBase)
	eff_path = []
	# eff_path code block
	for i in range(zone_dist[enemyBase]+1):
		eff_path.append(path[i])
	eff_path.reverse()
	
	# Strategy Decider
	if len(my_zone) > (zone_count // 3) or zone_dist[enemyBase] <= 5 :
		for i in range(len(pods)):
			atk_route = False
			for j in range(len(eff_path)):
				if eff_path[j] == pods[i][0] :
					pods_atk.append(pods[i])
					atk_route = True
			if atk_route == False :
				pods_def.append(pods[i])
	else:
		pods_def = pods.copy()
	
	
	# scatter out strategy
	for i in range(len(pods_def)):								# check every zone where we have pods
		avail_moves = moves(pods_def[i][0])						# moves available to do
		cap_moves = []										# capturing moves (neutral zones)
		xcap_moves = []										# not capping moves, to owned zones
		def_moves = []										# available defensive moves, array of linked zone that have fewest pods
		near_pods = []										# array of pods on linked zones (for intermediate variable in finding def_moves)
		
		# check if available moves is cap moves or not, and gives the array of cap_moves and xcap_moves
		for j in range(len(avail_moves)):
			owned=False
			for k in range(len(my_zone)):
				if my_zone[k] == avail_moves[j]:
					owned=True
			if owned == False:
				cap_moves.append(avail_moves[j])
			else:
				xcap_moves.append(avail_moves[j])
		
		# counting how many pods in xcap_moves, and gives the array of pods inside every zone in xcap_moves
		# Example :		xcap_moves	= [ 21, 47, 69, 99 ]
		# 				near_pods	= [  3, 12,  0,  7 ]
		# 				=> zone 21 have 3 pods, zone 47 have 12 pods, etc
		for j in range(len(xcap_moves)):
			no_pods = True
			for k in range(len(pods_def)):
				if pods_def[k][0] == xcap_moves[j]:
					no_pods = False
					zone_with_pods = k
			if no_pods == True:
				near_pods.append(0)
			else:
				near_pods.append(pods_def[zone_with_pods][1])
		
		# finding zone ID in xcap_moves with fewest pods, and listing it in def_moves
		for j in range(len(near_pods)):
			if near_pods[j] == min(near_pods):
				def_moves.append(xcap_moves[j])

		# calculating number of pods to be moved
		if pods_def[i][1] > 1:
			n_pods = int(pods_def[i][1]//2)
		else:
			n_pods = 1
		
		# moves to do, with priority cap_moves > def_moves. if found 2 posibility witf same priority, take random action
		if len(cap_moves) > 1:
			rdm_moves=cap_moves[random.randint(0, len(cap_moves)-1)]
			print(n_pods, str(pods_def[i][0]), str(rdm_moves), end=" ")
		elif len(cap_moves) == 1:
			rdm_moves=cap_moves[0]
			print(n_pods, str(pods_def[i][0]), str(rdm_moves), end=" ")
		else:
			if len(def_moves) == 1:
				rdm_moves=def_moves[0]
				print(n_pods, str(pods_def[i][0]), str(rdm_moves), end=" ")
			else:
				rdm_moves=def_moves[random.randint(0, len(def_moves)-1)]
				print(n_pods, str(pods_def[i][0]), str(rdm_moves), end=" ")
		
	# Invading strategy
	for i in range(len(pods_atk)):
		for j in range(len(eff_path)-1):
			if pods_atk[i][0] == eff_path[j] :
				print(str(pods_atk[i][1]), str(pods_atk[i][0]), str(eff_path[j+1]), end=" ")

	print()
	# first line for movement commands, second line no longer used (see the protocol in the statement for details)
	print("WAIT")

