import copy

def readFile(filename):
	with open(filename, "r") as file:
		return list(map(lambda x: int(x), file.readlines()))

def part1(adaptersInput):
	adapters = copy.copy(adaptersInput)
	adapters.sort()
	deviceRating = max(adapters)+3
	#print(f"Device Rating is {deviceRating}")

	differences = []
	currentRating = 0 #Start
	while currentRating+3 < deviceRating:
		for i in range(len(adapters)):
			adapter = adapters[i]
			if currentRating < adapter and adapter <= currentRating+3:
				difference =  adapter - currentRating
				differences.append(difference)
				#print(f"Current Rating is {currentRating} so adapter {adapter} would be acceptable, difference is {difference}")

				currentRating = adapter
				del adapters[i] # Remove adapter
				break
	differences.append(deviceRating - currentRating) # Final difference
		
	#print("Remaining adapters:", adapters)
	#print("Differences:")
	#for i in range(1,4):
	#	print(f"\t{differences.count(i)} differences of {i} jolt")
	print(f"Part 1: {differences.count(1)*differences.count(3)}")
	return differences.count(1)*differences.count(3)


def figure_ways(data):
	if len(data) == 0:
		return 0
	if len(data) < 3:
		return 1
	ways = 0
	ways += figure_ways(data[1:])
	ways += figure_ways(data[2:])
	ways += figure_ways(data[3:])
	return ways
	
def part2(adapters):
	adapters.append(0)
	adapters.sort()
	adapters.append(adapters[-1]+3)

	start = 0
	prev = 0
	paths = 1
	for i in range(len(adapters)):
		x = adapters[i]
		if prev + 3 == x:
			my_paths = figure_ways(adapters[start:i])
			#print(my_paths, adapters[start:i])
			paths *= my_paths
			start = i
		prev = adapters[i]
	print("Part 2:", paths)


if __name__ == "__main__":
	adapters = readFile("input.txt")
	part1(adapters)
	part2(adapters)