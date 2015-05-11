#!/usr/bin/env python
# -*- coding: utf-8 -*-

from goalscraper import getGoals
from goal import Goal
import operator
import math

#USAGE: python model.py 

roundScores = {'R16' : 0.825, 'Quarters' : 0.85, 'Semis' : 0.9, 'Finals' : 1}
timeScores = {}

#set a default year and initialize necessary variables
year = 2013

strYear = raw_input("Enter a year between 2009 & 2013 that you would like to analyze (please try 2013): ")
year = int(strYear)

weightedScores = {}
goals = {}
matches = {}
best = {}

#if incorrect input
while (year < 2009 or year > 2013):
	strYear = raw_input("Invalid input. Try again: ")
	year = int(strYear)

#call the goalscraper on this year
#this will return an array of Goal objects - which encapsulates:
#scorer, time, team, home/away, whether his team won, own team score & opposition score at the time of the goal
goalArray = getGoals(year)

print "Done collecting " + str(year) + " Goal data"

for goal in goalArray:

	weightedScores[goal.scorer] = 0
	goals[goal.scorer] = 0
	matches[goal.scorer] = 0
	best[goal.scorer] = 0

for goal in goalArray:
	#debug
	#if goal.scorer == 'Bale':
	#	print goal.scorer + " " + str(goal.time) + " " + str(goal.home) + " " + str(goal.ownTeamScore) + " " + str(goal.oppTeamScore) + " " + goal.round

	rs = 0.2*(roundScores[goal.round])

	t = int(goal.time)
	if t <= 15:
		x = 0.5
	elif t <= 30:
		x = 0.4
	elif t <= 45:
		x = 0.3
	elif t <= 60:
		x = 0.2
	elif t <= 75:
		x = 0.1
	else:
		x = 0.0
	ts = 0.15*(math.exp(-x))

	if goal.home:
		hs = 0.05*0.9
	else:
		hs = 0.05*1

	goalDiff = int(goal.ownTeamScore) - int(goal.oppTeamScore)
	dbl_GD = float(goalDiff)/10

	if goalDiff >= 0:
		gs = 0.6*(math.exp(-dbl_GD))
	else:
		dbl_GD = abs(dbl_GD)
		gs = 0.6*(math.exp(-(dbl_GD))+0.03)

	totalScore = rs + ts + hs + gs

	weightedScores[goal.scorer] += totalScore
	goals[goal.scorer] += 1
	best[goal.scorer] = max(totalScore, best[goal.scorer])

	if (goal.round == "Finals"):
		matches[goal.scorer] = max(4, matches[goal.scorer])
	elif (goal.round == "Semis"):
		matches[goal.scorer] = max(3, matches[goal.scorer])
	elif (goal.round == "Quarters"):
		matches[goal.scorer] = max(2, matches[goal.scorer])
	elif (goal.round == "R16"):
		matches[goal.scorer] = max(1, matches[goal.scorer])

for key in weightedScores.keys():
	goals[key] = weightedScores[key]/goals[key]
	matches[key] = weightedScores[key]/matches[key]

#sort the maps
sortedWG = sorted([(value,key) for (key,value) in weightedScores.items()])
sortedGA = sorted([(value,key) for (key,value) in goals.items()])
sortedMA = sorted([(value,key) for (key,value) in matches.items()])
sortedB = sorted([(value,key) for (key,value) in best.items()])

#for some reason, at this point, the names of the scorers gets messed up (while sorting)
#if its important to have those unmessed up, we'll have to sacrifice the sorted-ness
#but its whatever

print "\n Total Weighted Scores \n"
for element in sortedWG:
	print element #+ " " + str(sortedWG[key])

print "\n Goal Average \n"
for element in sortedGA:
	print element #+ " " + str(sortedWG[key]/goals[key])

#not very accurate. I'm assuming they've played all previous games when calculating
print "\n Match Average \n"
for element in sortedMA:
	print element #+ " " + str(sortedWG[key]/matches[key])

print "\n Best Score \n"
#this is the best score the player had
for element in sortedB:
	print element

