def readFile(filename):
	out = []
	with open(filename, "r") as file:
		for line in file.readlines():
			instruction, parameter = line.strip("\n").split(" ")
			out.append([instruction, int(parameter)])
	return out

def run(data):
	visitedInstructions = set()
	accumulator = 0
	index = 0
	
	while index < len(data):
		instruction, parameter = data[index]
		if index in visitedInstructions:
			return {"looping": True, "accumulator": accumulator}
		else:
			visitedInstructions.add(index)
			if instruction == "acc":
				accumulator += parameter
			elif instruction == "jmp":
				index += parameter-1
			index += 1
	return {"looping": False, "accumulator": accumulator}

def part1(data):
	print("Part 1:", run(data)["accumulator"])

def part2(data):
	for i in range(len(data)):
		if data[i][0] == "jmp": # Change jmp to nop
			data[i][0] = "nop"
			result = run(data)
			if not result["looping"]:
				print("Part 2:", result["accumulator"])
				return
			data[i][0] = "jmp" # Change back
		elif data[i][0] == "nop": # Change nop to jmp
			data[i][0] = "jmp"
			result = run(data)
			if not result["looping"]:
				print("Part 2:", result["accumulator"])
				return
			data[i][0] = "nop" # Change back

if __name__ == "__main__":
	data = readFile("input.txt")
	part1(data)
	part2(data)