class Goal:

	#instantiation with all necessary data
	def __init__(self, scorer, time, team, home, ownTeamScore, oppTeamScore, r):
		self.scorer = scorer
		self.time = time
		self.team = team
		self.home = home
		self.ownTeamScore = ownTeamScore
		self.oppTeamScore = oppTeamScore
		self.round = r
	
	#default constructor
	def __init__(self):
		self.scorer = ""
		self.time = 0
		self.team = ""
		self.ownTeamScore = 0
		self.oppTeamScore = 0
