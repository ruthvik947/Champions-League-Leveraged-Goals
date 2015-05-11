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

	rounds = {'r2l1' : ["R16 L1", 8] , 'r2l2' : ["R16 L2", 8], 
		's0l1' : ["Quarters L1", 4], 's0l2' : ["Quarters L2", 4], 
		't0l1' : ["Semis L1", 2], 't0l2' : ["Semis L2", 4],
		'u0' : ["Finals", 1]}

	goalArray = []

	temp = rYear-2000
	year = str(temp)+str(temp+1)

	goalTimeArray = {}
	rx = {}
	teamNo = 0
	htSquad = []
	atSquad = []
	homeTeam = ""
	awayTeam = ""
	hScore = 0
	aScore = 0

	for r in rounds.keys():

		#print "Parsing Round: " + rounds[r][0]

		url = "http://www.soccerassociation.com/CL/%s/%s.htm" % (year, r)
		#get request that ish
		while True:
			try:
				toScrape = requests.get(url)
				break
			except ConnectionError:
				print "Connection Error. Will try again"		

		#soup it too
		soup = BeautifulSoup(toScrape.content) 

		#this will give us the results section
		results = soup.findAll('table', { "cellspacing" : "1", "cellpadding" : "1"})[0]

		#this gives us the 
		teamsAndPlayers = results.findAll('td')

		#get all the teams playing
		#all the data we need is in 'td' tags but they aren't ordered by match
		rows = results.findAll('td')

		acount = 0
		hcount = 0
		awayGoal = False
		homeGoal = False

		#now we have each match to iterate through
		#if a 'td' tag with attributes align center and colspan is found, the a tags within have the team name

		for row in rows:

			if row.has_attr('align') and row.has_attr('colspan'):
				if row['align'] == 'center' and row['colspan'] == '2':

					#if we're here, we're looking at a new match (or the first one)
					#so now we make the goal objects and add to goalArray
					if teamNo%2==0:
						while len(goalTimeArray) > 0:

							#this will give us the min key in the array
							#this is also the first goal
							gt = 120
							for key in goalTimeArray.keys():
								#print goalTimeArray[key]
								if key <= gt:
									gt = key

							#now we have the smallest remaining value in the array at key = gt
							minScorer = goalTimeArray.pop(gt)
							rnd = rx.pop(gt)

							#if (homeTeam == 'Real Madrid'):
							#	print goalTimeArray[19]

							if any(minScorer in names for names in htSquad):

								print "Scorer: " + minScorer + " at minute " + str(gt)

								#for final, assume both teams are away
								if rounds[r][0] == 'Finals':
									newGoal = Goal(minScorer, gt, False, hScore, aScore, rnd)
								else:
									newGoal = Goal(minScorer, gt, True, hScore, aScore, rnd)
								goalArray.append(newGoal)

								hScore+=1

							elif any(minScorer in names for names in atSquad):

								print "Scorer: " + minScorer + " at minute " + str(gt)

								newGoal = Goal(minScorer, gt, False, aScore, hScore, rnd)
								goalArray.append(newGoal)

								aScore+=1


					#if teamNo%2 is 0 then home team, else away team. increment every time team is found
					#update homeTeam & awayTeam and get their squads
					#also set the scores to 0-0

					hScore = 0
					aScore = 0
					#goalTimeArray = {}

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

				if any(scorer in names for names in atSquad):
					#make the goal object now - note that it requires the score BEFORE the goal is scored
					#if this is the finals, assume Away

					if acount%2==0:
						goalTimeArray[gTime] = scorer
						rx[gTime] = rounds[r][0]
						#print "Scorer: " + scorer + " at minute " + str(gTime)
						#add time of the goal and the scorer to the goaltimearray
						#we need this because goals are not ordered by time on the website we're scraping from
					
					awayGoal = True
					homeGoal = False

				elif any(scorer in names for names in htSquad):

					if hcount%2==0:
						#print "Scorer: " + scorer + " at minute " + str(gTime)
						goalTimeArray[gTime] = scorer
						rx[gTime] = rounds[r][0]
						#print goalTimeArray[scorer]
					
					awayGoal = False
					homeGoal = True

				#all of this shpiel is because scorers get counted twice for some odd reason
				if awayGoal:
					acount+=1
				elif homeGoal:
					hcount+=1

	return goalArray





			