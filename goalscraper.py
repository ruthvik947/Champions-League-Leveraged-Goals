import requests
import sys
from bs4 import BeautifulSoup
import string
import re
from rosterscraper import getRoster
from goal import Goal

def getGoals (rYear):

	rounds = {'r2l1' : ["R16 L1", 8] , 'r2l2' : ["R16 L2", 8], 
		's0l1' : ["Quarters L1", 4], 's0l2' : ["Quarters L2", 4], 
		't0l1' : ["Semis L1", 2], 't0l2' : ["Semis L2", 4],
		'u0' : ["Finals", 1]}

	goalArray = []

	temp = rYear-2000
	year = str(temp)+str(temp+1)

	for r in rounds.keys():

		#print len(rounds)

		url = "http://www.soccerassociation.com/CL/%s/%s.htm" % (year, r)

		#get request that ish
		toScrape = requests.get(url)
		#soup it too
		soup = BeautifulSoup(toScrape.content)

		#this will give us the results section
		results = soup.findAll('table', { "cellspacing" : "1", "cellpadding" : "1"})[0]

		#get all the teams playing
		#all the data we need is in 'td' tags but they aren't ordered by match
		teamsAndPlayers = results.findAll('td', {"colspan" : "6", "align" : "center"})

		for x in range(0, len(teamsAndPlayers)):

			matches = (teamsAndPlayers[0]).findAll('td')

			teamNo = 0
			htSquad = []
			atSquad = []
			homeTeam = ""
			awayTeam = ""
			hScore = 0
			aScore = 0

			#now we have each match to iterate through
			print matches[x]

			for match in matches:

				#if a 'td' tag with attributes align center and colspan is found, the a tags within have the team name
				if match.has_attr({'align' : 'center'}) and match.has_attr({'colspan' : '2'}):

					#if teamNo%2 is 0 then home team, else away team. increment every time team is found
					#update homeTeam & awayTeam and get their squads
					#also set the scores to 0-0

					hScore = 0
					aScore = 0

					teamName = teamsAndPlayers[i].find('a')
					strTeamName = str(teamName)
					strTeamName = re.sub('<[^<]+?>', '', strTeamName)

					if (teamNo%2==0):
						homeTeam = strTeamName
						htSquad = getRoster(homeTeam, year)
					else:
						awayTeam = strTeamName
						atSquad = getRoster(awayTeam, year)

					teamNo+=1

				#if 'td' tag has attributes align right, then its a goal - this contains the goal time
				if teamsAndPlayers[i].has_attr({'align' : 'right'}):

					#for the name, look at the td tag immediately after the goal time thing
					#the a tags within that have the name of the team
					#check if player name is in htSquad or atSquad and increment scores accordingly
					#then create new instance of Goal class and add to array

					goalTime = str(teamsAndPlayers[i])
					goalTime = re.sub('<[^<]+?>', '', goalTime)

					gTime = int(goalTime)

					i+=1
					scorer = str(teamsAndPlayers)[i]
					scorer = re.sub('<[^<]+?>', '', scorer)

					if scorer in htSquad:
						#make the goal object now - note that it requires the score BEFORE the goal is scored
						#if this is the finals, assume Away
						if r == 'u0':
							newGoal = Goal(scorer, gTime, homeTeam, False, hScore, aScore, rounds[r][0])
						else:
							newGoal = Goal(scorer, gTime, homeTeam, True, hScore, aScore, rounds[r][0])
						goalArray.append(newGoal)
						hScore+=1

					elif scorer in atSquad:
						newGoal = Goal(scorer, gTime, homeTeam, False, hScore, aScore, r[0])
						goalArray.append(newGoal)
						aScore+=1

	return goalArray





			