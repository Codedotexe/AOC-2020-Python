import re
import sys
from copy import copy
from functools import cache

def readData(filename):
	with open(filename, "r") as file:
		rulesRaw, messages = file.read().split("\n\n")
	rulesRaw = rulesRaw.split("\n")
	messages = messages.split("\n")

	rules = dict()
	for ruleRaw in rulesRaw:
		ruleRaw  = ruleRaw.replace("\n", "")
		ruleName,sep,ruleBodyStr = ruleRaw.partition(":")

		ruleBody = []
		for i in ruleBodyStr.split("|"):
			i = i.strip(" ")
			ruleBody.append(i.split(" "))
		rules[ruleName] = ruleBody
	return rules, messages

@cache
def convertToRegex(startRule="0", recDepth=0, recLimit=-1):
	if recLimit != -1 and recDepth >= recLimit: # Fixed recursion depth limit
		return ""

	regex = ""
	parts = rules[startRule]
	for i in range(len(parts)):
		for subPart in parts[i]:
			if subPart.isdigit(): # Recurse
				temp = convertToRegex(startRule=subPart, recDepth=recDepth+1, recLimit=recLimit)
				if len(temp) > 1:
					regex += "(" + temp + ")"
				else:
					regex += temp
			else:
				regex += subPart.strip("\"")

		# If parts has a length greater than 1 and if i is not the last index
		if i+1 < len(parts): 
			regex += "|"
	return regex

def countMatchingMessages(pattern, messages):
	counter = 0
	for message in messages:
		if re.match(pattern, message):
			counter += 1
	return counter

def part1(rules, messages):
	regex = convertToRegex()
	pattern = re.compile("^"+regex+"$") # Completly match the pattern
	print(f"Part 1: {countMatchingMessages(pattern, messages)}/{len(messages)}")

def part2(rules, messages):
	origRules = copy(rules)
	rules["8"] = [["42"], ["42", "8"]]
	rules["11"] = [["42", "31"], ["42", "11", "31"]]
	# Now the rules have a loop

	regex = convertToRegex(recLimit=16) # A recLimit under 16 takes longer? and does not produce right value
	pattern = re.compile("^"+regex+"$") # Completly match the pattern
	#print("Pattern Size", int(sys.getsizeof(pattern)/1024), "KiB")
	counter = countMatchingMessages(pattern, messages)
	print(f"Part 2: {counter}/{len(messages)}")

	rules = origRules

if __name__ == "__main__":
	global rules
	rules, messages = readData("input.txt")
	part1(rules, messages)
	part2(rules, messages)