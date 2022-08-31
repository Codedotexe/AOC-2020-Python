from pprint import pprint
import itertools

def readData(filename):
	with open(filename, "r") as file:
		parts = file.read().split("\n\n")

	rules = []
	for ruleLine in parts[0].split("\n"):
		ruleName,sep,ruleMain = ruleLine.partition(":")
		ruleConditions = []
		for ruleCond in ruleMain.split(" or "):
			temp = ruleCond.split("-")
			ruleConditions.append([int(temp[0]), int(temp[1])])

		rules.append([ruleName, ruleConditions])

	yourTicket = []
	for i in parts[1].split("\n")[1].split(","):
		yourTicket.append(int(i))

	nearbyTickets = []
	for i in parts[2].split("\n")[1:]:
		temp = []
		for j in i.split(","):
			temp.append(int(j))
		nearbyTickets.append(temp)

	return rules, yourTicket, nearbyTickets

def part1(rules, nearbyTickets):
	# Flatten our rules
	simplifiedRules = []
	for rule in rules:
		simplifiedRules += rule[1]

	invalidNumbers = []
	indicesToBeRemoved = []
	for i in range(len(nearbyTickets)):
		for ticketNum in nearbyTickets[i]:
			for rule in simplifiedRules:
				if rule[0] <= ticketNum and rule[1] >= ticketNum:
					break
			else:
				invalidNumbers.append(ticketNum)
				indicesToBeRemoved.append(i)

	shortendNearbyTickets = []
	for i in range(len(nearbyTickets)):
		if i not in indicesToBeRemoved:
			shortendNearbyTickets.append(nearbyTickets[i])
	print("Part1:", sum(invalidNumbers))
	return shortendNearbyTickets

def findRulePos(rule, correctTickets, rulesLength):
	positions = []
	for pos in range(rulesLength):
		ok = True
		for ticket in correctTickets:
			anySubRuleMatching = False
			for subRule in rule[1]:
				if subRule[0] <= ticket[pos] and subRule[1] >= ticket[pos]:
					anySubRuleMatching = True
					break
			if not anySubRuleMatching:
				ok = False
				break
		if ok:
			positions.append(pos)
	return positions

def solveRulesIndicesProblem(rulesPossibleIndices, rulesIndices, rulesIndicesQueue): #Solve Rules Indices Problem with backtracking
	if rulesIndicesQueue == []:
		return True
	for key in rulesPossibleIndices.keys():
		if key not in rulesIndices:
			if rulesIndicesQueue[0] in rulesPossibleIndices[key]:
				index = rulesIndicesQueue.pop(0)
				rulesIndices[key] = index
				if solveRulesIndicesProblem(rulesPossibleIndices, rulesIndices, rulesIndicesQueue):
					return True
				else:
					rulesIndices.pop(key)
					rulesIndicesQueue.append(index)
	return False

def part2(rules, correctTickets, yourTicket):
	rulesPossibleIndices = dict()
	for rule in rules:
		rulesPossibleIndices[rule[0]] = findRulePos(rule, correctTickets, len(rules))

	rulesIndices = dict()
	if solveRulesIndicesProblem(rulesPossibleIndices, rulesIndices, list(range(len(rules)))):
		out = 1
		for key, val in rulesIndices.items():
			if "departure" in key:
				out *= yourTicket[val]
		print("Part2:", out)
	else:
		print("Found no possible way to arrange rules Indices so that every rule has an unique index")

if __name__ == "__main__":
	rules, yourTicket, nearbyTickets = readData("input.txt")
	correctTickets = part1(rules, nearbyTickets)
	part2(rules, correctTickets, yourTicket)
