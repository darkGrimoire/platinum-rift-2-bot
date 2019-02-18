import sys
import math
#adfasdfa
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
links1 = []
links2 = []
for i in range(link_count):
	zone_1, zone_2 = [int(j) for j in input().split()]
	links1.append(zone_1)
	links2.append(zone_2)

# VAR
enemyBase = -1
myBase = -1

# MOVEMENT_BASIC
def moves(x):
	aval = []
	for i in range(len(links1)):
		if x == links1[i]:
			aval.append(links2[i])
	for i in range(len(links2)):
		if x == links2[i]:
			aval.append(links1[i])
	return aval
# CHECKS

# game loop
while True:
	command=""
	vis_zone = []
	pods = []
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
			vis_zone.append(z_id)
			if enemyBase == -1 and owner_id == 1:
				enemyBase = z_id
		if pods_p0 > 0:
			pods.append(z_id)
			if myBase == -1:
				myBase = z_id
	print(vis_zone, file=sys.stderr)
	#print(links1, file=sys.stderr)
	#print(links2, file=sys.stderr)
	print(pods, file=sys.stderr)
	print(moves(pods[0]), file=sys.stderr)
	print(enemyBase,myBase, file=sys.stderr)
	# first line for movement commands, second line no longer used (see the protocol in the statement for details)
	#print(str() + " " + str() + " " + str())
	availableMove = moves(pods[0])
	print("10 " + str(pods[0]) + " " + str(max(availableMove)))
	print("10 14 21")
	print("WAIT")
