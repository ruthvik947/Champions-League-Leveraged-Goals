#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import sys
from bs4 import BeautifulSoup
import string
import re
from requests.exceptions import ConnectionError


keyMap = {'FC Schalke 04' : ['ger', 'bundes', 'schalke'], 
		'Celtic' : ['scots', 'scotprem', 'celtic'], 
		'Manchester City' : ['eng', 'faprem', 'mancity'], 
		'Arsenal' : ['eng', 'faprem', 'arsenal'], 
		'Manchester United' : ['eng', 'faprem', 'manutd'], 
		'Chelsea' : ['eng', 'faprem', 'chelsea'], 
		'Liverpool' : ['eng', 'faprem', 'liverpool'],
		'Tottenham Hotspur' : ['eng', 'faprem', 'tottenha'],
		'Paris SG' : ['france', 'ligue1', 'psg'],
		'Lyon' : ['france', 'ligue1', 'lyon'],
		'Marseille' : ['france', 'ligue1', 'marseille'],
		'Bordeaux' : ['france', 'ligue1', 'bordeaux'],
		'Barcelona' : ['spain', 'laliga', 'barce'],
		'Atlético Madrid' : ['spain', 'laliga', 'amadrid'],
		'Real Madrid' : ['spain', 'laliga', 'rmadrid'],
		'Valencia' : ['spain', 'laliga', 'valencia'],
		'Málaga' : ['spain', 'laliga', 'malaga'],
		'Sevilla' : ['spain', 'laliga', 'sevilla'],
		'Bayer Leverkusen' : ['ger', 'bundes', 'bayerlev'],
		'Bayern München' : ['ger', 'bundes', 'bayern'],
		'Borussia Dortmund' : ['ger', 'bundes', 'dortmund'],
		'VfB Stuttgart' : ['ger', 'bundes', 'stuttg'],
		'Milan' : ['italy', 'seriea', 'milan'],
		'Juventus' : ['italy', 'seriea', 'juventus'],
		'Napoli' : ['italy', 'seriea', 'napoli'],
		'Inter' : ['italy', 'seriea', 'inter'],
		'Roma' : ['italy', 'seriea', 'roma'],
		'Fiorentina' : ['italy', 'seriea', 'fiorenti'],
		'Zenit' : ['russia', 'rfpl', 'zenit'],
		'CSKA' : ['russia', 'rfpl', 'cska'],
		'Olympiakos' : ['greece', 'superl', 'olympiak'],
		'Galatasaray' : ['turkey', 'superl', 'gala'],
		'Shakhtar' : ['ukraine', 'upl', 'shakhtar'],
		'FC Porto' : ['portugal', 'primeira', 'porto'],
		'Benfica' : ['portugal', 'primeira', 'benfica'],
		'FC Basel' : ['switz', 'superl', 'basel'],
		'FC København' : ['denmark', 'supliga', 'koben'],}

def getRoster(team, rYear):

	#empty set of players intially
	squad = []

	year = str(rYear) + "-" + str(rYear+1)

	#=nation, year, league, squad
	#CL squads may not be exactly the same as domestic squads but domestic squads cover the entire roster

	url = "http://www.footballsquads.co.uk/%s/%s/%s/%s.htm" % (keyMap[team][0], year, keyMap[team][1], keyMap[team][2])

	#http get to this url
	while True:
		try:
			toScrape = requests.get(url)
			break
		except ConnectionError:
			print "Connection Error. Will try again"

	soup = BeautifulSoup(toScrape.content)

	#these are all the divs with player names
	players = soup.findAll('td', {'width' : '180'})

	for p in players:

		#convert each player name to string 
		playerStr = str(p)

		#get rid of the nasty tags
		playerStr = re.sub('<[^<]+?>', '', playerStr)
		
		#sometimes the name is Name and sometimes it's an empty div. We don't want that in our roster
		#also the second time we find name, they list out players who aren't at the club
		count = 0
		if(playerStr != ""):
			if (playerStr == "Name" and count == 0):
				count+=1
			elif (playerStr == "Name" and count > 0):
				break
			else:
				squad.append(playerStr)

	return squad