from goalscraper import getGoals
from goal import Goal

#set a default year and initialize necessary variables
year = 2013

strYear = raw_input("Enter a year between 2009 & 2013 that you would like to analyze: ")
year = int(strYear)

#if incorrect input
while (year < 2009 or year > 2013):
	strYear = raw_input("Invalid input. Try again: ")
	year = int(strYear)

#call the goalscraper on this year
#this will return an array of Goal objects - which encapsulates:
#scorer, time, team, home/away, whether his team won, own team score & opposition score at the time of the goal
goalArray = getGoals(year)



