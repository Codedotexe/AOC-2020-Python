def readData(filename):
	with open(filename, "r") as file:
		data = file.read().split(",")
		return list(map(lambda x: int(x), data))

def simulate(numbers, totalTurns):
	dictionary = dict()
	numbersLength = len(numbers)
	for i in range(len(numbers)-1):
		dictionary[numbers[i]] = i+1


	lastSpoken = numbers[numbersLength-1]
	for t in range(numbersLength+1, totalTurns+1):
		temp = lastSpoken
		if lastSpoken in dictionary:
			lastSpoken = (t-1) - dictionary[lastSpoken]
		else:
			dictionary[lastSpoken] = t-1
			lastSpoken = 0
		dictionary[temp] = t-1
	return lastSpoken


if __name__ == "__main__":
	numbers = readData("input.txt")
	print("Starting Numbers:", numbers)

	print(simulate(numbers, 2020))
	print(simulate(numbers, 30000000)) # Can take up to 30sec
