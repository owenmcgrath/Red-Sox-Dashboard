import mlbgame

import twitter

from Twitter_API_Key_Info import *

import datetime

import threading

import os

api = twitter.Api(consumer_key = consumer_key,
				  consumer_secret = consumer_secret,
				  access_token_key = access_token_key,
				  access_token_secret = access_token_secret)


def getPlayer(playerID, playerlist):
	for p in playerlist:
		if p.id == playerID:
			return p
	return 0

def getTweet(handle):
	tweets = api.GetUserTimeline(screen_name = handle)
	return tweets[0].text

def printStandings(div):
	print("\nSTANDINGS\n=========\n")
	for t in div.teams:
		print(t.team_abbrev + " " + str(t.w) + " " + str(t.l) + " " + str(t.gb))

def printUpcomingGame(game):
	print("\nUPCOMING GAME\n=============\n")
	print(game.home_team + " vs. " + game.away_team )
	print(game.game_start_time)
	print(game.p_pitcher_home + " vs. " + game.p_pitcher_away)

def printFinalScore(game):
	print("\nFINAL SCORE\n===========\n")
	print(game.home_team + " " + str(game.home_team_runs))
	print(game.away_team + " " + str(game.away_team_runs))
	print("W: " + str(game.w_pitcher) + " " + str(game.w_pitcher_wins) + "-" + str(game.w_pitcher_losses))
	print("L: " + str(game.l_pitcher) + " " + str(game.l_pitcher_wins) + "-" + str(game.l_pitcher_losses))

def printCurrentGame(game):
	print("\nCURRENT GAME INFO\n=================\n")
	current_inning = mlbgame.game_events(game.game_id)[-1]
	players = mlbgame.players(game.game_id)
	playerlist = players.home_players + players.away_players

	if len(current_inning.bottom) > 0:
		print("Bottom " + str(current_inning) + "\n")
		last_ab = current_inning.bottom[-1]
	elif len(current_inning.top) > 0:
		print("Top " + str(current_inning) + "\n")
		last_ab = current_inning.top[-1]
	else :  
		print("Upcoming " + str(current_inning) + "\n")
		current_inning = mlbgame.game_events(game.game_id)[-2]
		last_ab = current_inning.bottom[-1]

	pitcher = getPlayer(last_ab.pitcher, playerlist)
	batter = getPlayer(last_ab.batter, playerlist)

	pitcherStatus = pitcher.team_abbrev + " " + "Pitching: " + pitcher.first + " " + pitcher.last + ", ERA: " + ("%.2f"%pitcher.era)
	batterStatus = batter.team_abbrev + " " + "Batting: " + batter.first + " " + batter.last + ", AVG: " + ("%.3f"%batter.avg)[1:]

	print(pitcherStatus)
	print(batterStatus)

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
	print("\n" + str(last_ab.o) + " Out(s), " + base_status + "\n")
	print("SCORE\n=====\n" + game.home_team+ ": " + str(game.home_team_runs) + "\n" + game.away_team + ": " + str(game.away_team_runs))


def printTweets():
	print("\nTWEETS\n======\n")
	print("Alex Speier (@alexspeier): " + getTweet("alexspeier"))
	print("\nJared Carrabis (@Jared_Carrabis): " + getTweet("Jared_Carrabis"))
	print("\nMLB (@mlb): " + getTweet("mlb"))
	print("\nRed Sox (@redsox): " + getTweet("RedSox"))

def looper():
	os.system('cls')
	threading.Timer(10.0, looper).start()
	gameday = datetime.datetime.now()
	# tomorrow = gameday - datetime.timedelta(1)

	noGameFound = True

	while noGameFound:
			#check for game gameday
		if len(mlbgame.day(gameday.year, gameday.month, gameday.day, home='Red Sox', away = 'Red Sox')) != 0:
			game = mlbgame.day(gameday.year, gameday.month, gameday.day, home='Red Sox', away = 'Red Sox')[0]
			noGameFound = False
			#if no game on the current day check on the next day
		else:
			gameday += datatime.timedelta(1)



	standings = mlbgame.standings()
	alEast = standings.divisions[3]

	#game is over, display final score
	if(game.game_status == "FINAL"):
		printStandings(alEast)
		printFinalScore(game)
		printTweets()

	#display upcoming game info + standings 
	elif(game.game_status == "PRE_GAME"):
		printStandings(alEast)
		printUpcomingGame(game)
		printTweets()

	#game is on, display live game info
	else:
		printCurrentGame(game)

looper()

