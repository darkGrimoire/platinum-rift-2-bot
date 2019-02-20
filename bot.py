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

links1 = []		#array for linked zone
links2 = []
for i in range(link_count):									#sys
	zone_1, zone_2 = [int(j) for j in input().split()]		#sys
	links1.append(zone_1)									#collecting data of linked zone in links1 and links2
	links2.append(zone_2)									#zone with id links1[i] are connected to zone links2[i]

# VAR
if my_id == 0:
	enemy_id=1
else:
	enemy_id=0
enemyBase = -1
myBase = -1

# MOVEMENT_BASIC
def moves(x):							#input a zone ID and gives back the adjacent zone in an array
	aval = []
	for i in range(len(links1)):
		if x == links1[i]:
			aval.append(links2[i])
	for i in range(len(links2)):
		if x == links2[i]:
			aval.append(links1[i])
	return aval

# game loop
while True:
	vis_zone = []
	pods = []
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
			vis_zone.append(z_id)								#array of visible zone
			if enemyBase == -1 and owner_id == enemy_id:		#sets the enemyBase zone ID
				enemyBase = z_id	
			if myBase == -1 and owner_id == my_id:				#sets myBase zone ID, works same like enemyBase
				myBase = z_id									#the (enemyBase == -1) part makes this only true at game beginning, when enemyBase=-1 (see #VAR)
			if owner_id == my_id:
				my_zone.append(z_id)							#array of zone owned
		if my_id == 0:
			if pods_p0 > 0:
				pods.append([z_id, pods_p0, pods_p1])				#array of pods located: [location, number of pods: player 0(me), player 1]
		else:
			if pods_p1 > 0:
				pods.append([z_id, pods_p1, pods_p0])				#array of pods located: [location, number of pods: player 1(me), player 0]

	# Write an action using print
	# To debug: print("Debug messages...", file=sys.stderr)
	
	# scatter out strategy
	for i in range(len(pods)):								# check every zone where we have pods
		avail_moves = moves(pods[i][0])						# moves available to do
		cap_moves = []										# capturing moves (neutral zones)
		xcap_moves = []										
		def_moves = []										# available defensive moves, array of linked zone that have fewest pods
		near_pods = []										# array of pods on linked zones (for intermediate variable in finding def_moves)
		for j in range(len(avail_moves)):
			owned=False
			for k in range(len(my_zone)):
				if my_zone[k] == avail_moves[j]:
					owned=True
			if owned == False:
				cap_moves.append(avail_moves[j])
			else:
				xcap_moves.append(avail_moves[j])
		for j in range(len(xcap_moves)):
			no_pods = True
			for k in range(len(pods)):
				if pods[k][0] == xcap_moves[j]:
					no_pods = False
					zone_with_pods = k
			if no_pods == True:
				near_pods.append(0)
			else:
				near_pods.append(pods[zone_with_pods][1])
		for j in range(len(near_pods)):
			if near_pods[j] == min(near_pods):
				def_moves.append(xcap_moves[j])

		if pods[i][1] > 1:
			n_pods = int(pods[i][1]//2)
		else:
			n_pods = 1
		if len(cap_moves) > 1:
			rdm_moves=cap_moves[random.randint(0, len(cap_moves)-1)]
			print(n_pods, str(pods[i][0]), str(rdm_moves), end=" ")
		elif len(cap_moves) == 1:
			rdm_moves=cap_moves[0]
			print(n_pods, str(pods[i][0]), str(rdm_moves), end=" ")
		else:
			if len(def_moves) == 1:
				rdm_moves=def_moves[0]
				print(n_pods, str(pods[i][0]), str(rdm_moves), end=" ")
			else:
				rdm_moves=def_moves[random.randint(0, len(def_moves)-1)]
				print(n_pods, str(pods[i][0]), str(rdm_moves), end=" ")

	print()
	# first line for movement commands, second line no longer used (see the protocol in the statement for details)
	print("WAIT")

