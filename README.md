# Bot Platinum Rift 2

Bot programming untuk tugas Day 3 Sekuro ITB 2019
username codingame: wolfphysics
[>Link Codingame Klik Disini<](https://www.codingame.com/ide/puzzle/platinum-rift-episode-2)

## Kontributor: 
* Faris Rizki Ekananda (16518245)
* Farrel Dzaudan Naufal (16718004)
* Eva Silvia Septiana (16018097)
* Rayhan Aby Imtiyaz (16518261)

## Penjelasan Kode
1. Import modul-modul yang akan dipakai.
```
import sys
import math
import random
```
2. Input sistem: zone_id dan platinum_source
```
player_count, my_id, zone_count, link_count = [int(i) for i in input().split()]
for i in range(zone_count):
	zone_id, platinum_source = [int(j) for j in input().split()]
```
3. Links: Mengambil informasi tentang hubungan antarzona
```
links1 = []		#array for linked zone
links2 = []
for i in range(link_count):		
	zone_1, zone_2 = [int(j) for j in input().split()]
	links1.append(zone_1)
	links2.append(zone_2)
```
4. Inisialisasi variabel-variabel yang akan digunakan dalam bot yang hanya di-set sekali per game.
```
if my_id == 0:
	enemy_id=1
else:
	enemy_id=0
enemyBase = -1
myBase = -1
```
5. Mencari tahu tile-tile disebelah x dengan memanfaatkan Links
```
def moves(x):							#input a zone ID and gives back the adjacent zone in an array
	aval = []
	for i in range(len(links1)):
		if x == links1[i]:
			aval.append(links2[i])
	for i in range(len(links2)):
		if x == links2[i]:
			aval.append(links1[i])
	return aval
```
6. Mengambil informasi-informasi berupa: HQ (dilakukan sekali per game), dimana letak pods kita dan musuh serta ada berapa saja.
```
vis_zone = []
	pods = []
	my_zone = []
	my_platinum = int(input())
	for i in range(zone_count):
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
				pods.append([z_id, pods_p1, pods_p0])
```
7. Strategi "Scatter-out". Bagian pertama mencari tahu tentang:
* cap_moves: list zona yang belum kita miliki disekitar pods yg bersangkutan
* xcap_moves: list zona yang sudah kita miliki disekitar pods yg bersangkutan
* def_moves: Apabila zona disekitar pods sudah dimiliki semua, pods akan mencari zona mana yang paling sedikit jumlah podsnya.
* near_pods: berapa jumlah pods disekitar pods yang ditinjau

Bagian kedua menentukan gerakan pods berdasarkan prioritas: cap_moves, lalu def_moves. Apabila pilihan gerakan di list moves lebih dari satu maka gerakan akan dibuat secara random.
```
for i in range(len(pods)):								# check every zone where we have pods
		avail_moves = moves(pods[i][0])						# moves available to do
		cap_moves = []										# capturing moves (neutral zones)
		xcap_moves = []										
		def_moves = []										# available defensive moves, array of linked zone that have fewest pods
		near_pods = []										# array of pods on linked zones (for intermediate variable in finding def_moves)
# Bagian 1
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
		# Bagian 2		
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
```
