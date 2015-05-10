#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import sys
from bs4 import BeautifulSoup
import string
import re
from rosterscraper import getRoster
from goal import Goal
import urllib
from  __builtin__ import any
import time
from requests.exceptions import ConnectionError

def getGoals (rYear):

	rounds = {'r2l1' : ["R16", 8] , 'r2l2' : ["R16", 8], 
		's0l1' : ["Quarters", 4], 's0l2' : ["Quarters", 4], 
		't0l1' : ["Semis", 2], 't0l2' : ["Semis", 4],
		'u0' : ["Finals", 1]}

	goalArray = []

	temp = rYear-2000
	year = str(temp)+str(temp+1)

	for r in rounds.keys():

		print "Parsing Round: " + rounds[r][0]

		url = "http://www.soccerassociation.com/CL/%s/%s.htm" % (year, r)
		#get request that ish
		while True:
			try:
				toScrape = requests.get(url)
				break
			except ConnectionError:
				print "Connection Error. Will try again"		#soup it too

		soup = BeautifulSoup(toScrape.content) 

		#this will give us the results section
		results = soup.findAll('table', { "cellspacing" : "1", "cellpadding" : "1"})[0]

		#this gives us the 
		teamsAndPlayers = results.findAll('td')

		teamNo = 0
		htSquad = []
		atSquad = []
		homeTeam = ""
		awayTeam = ""
		hScore = 0
		aScore = 0
		acount = 0
		hcount = 0
		awayGoal = False
		homeGoal = True

		#get all the teams playing
		#all the data we need is in 'td' tags but they aren't ordered by match
		rows = results.findAll('td')

		#now we have each match to iterate through
		#if a 'td' tag with attributes align center and colspan is found, the a tags within have the team name

		for row in rows:

			if row.has_attr('align') and row.has_attr('colspan'):
				if row['align'] == 'center' and row['colspan'] == '2':

					#if teamNo%2 is 0 then home team, else away team. increment every time team is found
					#update homeTeam & awayTeam and get their squads
					#also set the scores to 0-0

					hScore = 0
					aScore = 0

					teamName = row.find('a')

					strTeamName = str(teamName)
					strTeamName = re.sub('<[^<]+?>', '', strTeamName)
 
					if (teamNo%2==0):
						homeTeam = strTeamName
						htSquad = getRoster(homeTeam, rYear)
					else:
						awayTeam = strTeamName
						atSquad = getRoster(awayTeam, rYear)

					teamNo+=1

			#if 'td' tag has attributes align right, then its a goal - this contains the goal time
			elif row.has_attr('align') and row['align'] == 'right':

				#for the name, look at the td tag immediately after the goal time thing
				#the a tags within that have the name of the team
				#check if player name is in htSquad or atSquad and increment scores accordingly
				#then create new instance of Goal class and add to array

				goalTime = str(row)
				goalTime = re.sub('<[^<]+?>', '', goalTime)
				goalTime = goalTime.replace('(p)', '')

				#we dont want own goals to count for anything
				if ('(og)' not in goalTime):
					gTime = int(goalTime)

			elif (len(row.findAll('a')) > 0) and not row.has_attr('bgcolor'):

				scorer = row.find('a')

				scorer = str(scorer)
				scorer = re.sub('<[^<]+?>', '', scorer)

				if any(scorer in names for names in htSquad):
					#make the goal object now - note that it requires the score BEFORE the goal is scored
					#if this is the finals, assume Away

					if hcount%2==0:

						print "Scorer: " + scorer + " at minute " + str(gTime)

						if r == 'u0':
							newGoal = Goal(scorer, gTime, homeTeam, False, hScore, aScore, rounds[r][0])
						else:
							newGoal = Goal(scorer, gTime, homeTeam, True, hScore, aScore, rounds[r][0])
						goalArray.append(newGoal)
						hScore+=1

					homeGoal = True
					awayGoal = False

				elif any(scorer in names for names in atSquad):

					if acount%2==0:

						print "Scorer: " + scorer + " at minute " + str(gTime)

						newGoal = Goal(scorer, gTime, homeTeam, False, hScore, aScore, rounds[r][0])
						goalArray.append(newGoal)
						aScore+=1

					awayGoal = True
					homeGoal = False

				#all of this shpiel is because scorers get counted twice for some odd reason
				if awayGoal:
					acount+=1
				elif homeGoal:
					hcount+=1



	return goalArray





			