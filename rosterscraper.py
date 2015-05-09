import requests
import sys
from bs4 import BeautifulSoup
import string
import re
from rosters import *

def getRoster(team, rYear):

	#empty set of players intially
	squad = []

	year = str(rYear) + "-" + str(rYear+1)

	#=nation, year, league, squad
	#CL squads may not be exactly the same as domestic squads but domestic squads cover the entire roster
	url = "http://www.footballsquads.co.uk/%s/%s/%s/%s.htm" % (keyMap[team][0], year, keyMap[team][1], keyMap[team][2])

	#http get to this url
	toScrape = requests.get(url)

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