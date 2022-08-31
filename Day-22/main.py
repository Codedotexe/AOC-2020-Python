from pprint import pprint
from copy import copy
import logging
import sys

def parseDeckString(deckString):
	deck = []
	for line in deckString.split("\n"):
		if line.isdigit():
			deck.append(int(line))
	return deck

def readFile(filePath):
	with open(filePath, "r") as file:
		deck1Str, deck2Str = file.read().split("\n\n") # Split on empty line
	return parseDeckString(deck1Str), parseDeckString(deck2Str)

def cardScore(cardDeck):
	hash = 0
	for i in range(len(cardDeck)):
		hash += (len(cardDeck)-i) * cardDeck[i]	
	return hash

def part1(deck1, deck2):
	deck1 = copy(deck1)
	deck2 = copy(deck2)
	roundCounter = 0
	while deck1 != [] and deck2 != []:
		p1Top = deck1.pop(0)
		p2Top = deck2.pop(0)
		if p1Top > p2Top:
			deck1.append(p1Top)
			deck1.append(p2Top)
		else:
			deck2.append(p2Top)
			deck2.append(p1Top)
		roundCounter += 1
	
	if deck1 == []:
		winner = 2
	elif deck2 == []:
		winner = 1
	else:
		winner = 0

	logging.info(f"Part 1: Winner is player {winner} with score {cardScore(deck1 + deck2)}")

def recursiveCombat(deck1, deck2, gameNumber=1):
	previousRoundDecks = set()
	roundNumber = 1
	while deck1 != [] and deck2 != []:
		logging.debug(f"-- Round {roundNumber} (Game {gameNumber}) --")

		logging.debug("deck1", deck1)
		logging.debug("deck2", deck2)
		p1Top = deck1.pop(0)
		p2Top = deck2.pop(0)
		logging.debug("p1-top", p1Top)
		logging.debug("p2-top", p2Top)
		
		if tuple(deck1+deck2) in previousRoundDecks: # Win for player 1
			deck1.append(p1Top)
			deck1.append(p2Top)
			logging.debug(f"Player 1 won the game {gameNumber} (recursion break)")
			return 1 # End game, winner is player 1 as in definition

		previousRoundDecks.add(tuple(deck1+deck2)) # Add current deck hash

		if len(deck1) >= p1Top and len(deck2) >= p2Top: # Play a recursive subgame
			logging.debug("Playing a subgame")
			winner = recursiveCombat(deck1[:p1Top], deck2[:p2Top], gameNumber=gameNumber+1)
		else:
			if p1Top > p2Top:
				winner = 1
			else:
				winner = 2
		
		if winner == 1:
			deck1.append(p1Top)
			deck1.append(p2Top)
		elif winner == 2:
			deck2.append(p2Top)
			deck2.append(p1Top)

		logging.debug(f"Player {winner} won the round {roundNumber} in game {gameNumber}")
		roundNumber += 1

	logging.debug(f"Player {winner} won the game {gameNumber}")
	return winner # End game

def part2(deck1, deck2):
	winner = recursiveCombat(deck1, deck2)
	logging.debug(f"Deck 1: {deck1}")
	logging.debug(f"Deck 2: {deck2}")
	logging.info(f"Part 2: Winner is player {winner} with score {cardScore(deck1+deck2)}")
	
if __name__ == "__main__":
	logging.basicConfig(stream=sys.stdout, level=logging.INFO)
	#deck1, deck2 = readFile("input_test.txt")
	deck1, deck2 = readFile("input.txt")

	logging.debug(deck1)
	logging.debug(deck2)

	part1(deck1, deck2)
	part2(deck1, deck2)

