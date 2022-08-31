def readFile(filename):
	with open(filename, "r") as file:
		data = file.read()

	out = []
	for i in data.split("\n\n"):
		temp = []
		for j in i.split("\n"):
			temp.append(set(j))
		out.append(temp)
	return out

def part1(data):
	mySum = 0
	for group in data:
		x = set()
		for person in group:
			x.update(person)
		mySum += len(x)
	print("Part 1:", mySum)

def part2(data):
	count = 0
	for group in data:
		count += len(set.intersection(*group))
	print("Part 2:", count)

if __name__ == "__main__":
	data = readFile("input.txt")
	part1(data)
	part2(data)