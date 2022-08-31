import re

def readFile(filename):
	with open(filename, "r") as file:
		lines = file.readlines()

	output = []
	pattern = re.compile("(\\d+)-(\\d+) (.): (.+)")
	for line in lines:
		match = re.search(pattern, line).groups()
		output.append([int(match[0]), int(match[1]), match[2], match[3]])
	return output

def part1(policies):
	meetCriteria = 0
	for policy in policies:
		count = policy[3].count(policy[2])
		if policy[0] <= count and policy[1] >= count:
			meetCriteria += 1
	print("Part 1:", meetCriteria)

def part2(policies):
	meetCriteria = 0
	for policy in policies:
		pos1 = policy[0]-1 #Orig pos does not have index 0
		pos2 = policy[1]-1
		letter = policy[2]
		password = policy[3]
		if (password[pos1] == letter) ^ (password[pos2] == letter):
			meetCriteria += 1
	print("Part 2:", meetCriteria)

if __name__ == "__main__":
	policies = readFile("input.txt")
	part1(policies)
	part2(policies)
	