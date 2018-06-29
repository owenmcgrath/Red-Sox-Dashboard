import mlbgame

import datetime


def getPlayer(playerID, playerlist):
	for p in playerlist:
		if p.id == playerID:
			return p
	return 0




current_datetime = datetime.datetime.now()
print("got time")

game = mlbgame.day(current_datetime.year, current_datetime.month, current_datetime.day, home='Red Sox')[0]
print("got game")

current_inning = mlbgame.game_events(game.game_id)[-1]
print("got inning")

players = mlbgame.players(game.game_id)
playerlist = players.home_players + players.away_players
print("got players")

overview = mlbgame.overview(game.game_id)
print("got overview")

standings = mlbgame.standings()
alEast = standings.divisions[3]
print("got standings \n\n")

print("\nSTANDINGS\n=========\n")

for t in alEast.teams:
	print(t.team_abbrev + " " + str(t.w) + " " + str(t.l) + " " + str(t.gb))

playerlist = players.home_players + players.away_players

print("\nSOX GAME INFO\n=============\n")


if len(current_inning.bottom) > 0:
	last_ab = current_inning.bottom[-1]
elif len(current_inning.top) > 0:
	last_ab = current_inning.top[-1]
else :  
	print("Inbetween Innings")
	current_inning = mlbgame.game_events(game.game_id)[-2]
	last_ab = current_inning.bottom[-1]

pitcher = getPlayer(last_ab.pitcher, playerlist)
batter = getPlayer(last_ab.batter, playerlist)

pitcherStatus = pitcher.team_abbrev + " " + "Pitching: " + pitcher.first + " " + pitcher.last + ", ERA: " + ("%.2f"%pitcher.era)
batterStatus = batter.team_abbrev + " " + "Batting: " + batter.first + " " + batter.last + ", AVG: " + ("%.3f"%batter.avg)[1:]

print(pitcherStatus)
print(batterStatus)

# print(last_ab.__dict__)



if(last_ab.b1 or last_ab.b2 or last_ab.b3):
	base_status = "Runners on: "
else : 
	base_status = "No Runners On"
if last_ab.b1:
	base_status += "First "
if last_ab.b2:
	base_status += "Second "
if last_ab.b3:
	base_status += "Third"
print("\n" + str(last_ab.o) + " Outs, " + base_status + "\n")

#print(overview.__dict__)

print("SCORE\n=====\n" + overview.home_team_name + ": " + str(overview.home_team_runs) + "\n" + overview.away_team_name + ": " + str(overview.away_team_runs))
print()
