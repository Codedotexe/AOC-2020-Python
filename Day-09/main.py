def readFile(filename):
	with open(filename, "r") as file:
		return list(map(lambda x: int(x), file.readlines()))

def findInvalidNumber(data, preambleLength=25):
	for i in range(preambleLength, len(data)):
		ok = False
		for j in range(i, i-preambleLength-1, -1):
			for k in range(i, i-preambleLength-1, -1):
				if data[j] != data[k] and data[j]+data[k] == data[i]:
					#print(f"{data[j]} + {data[k]} = {data[i]}")
					ok = True
					break
		if not ok:
			return data[i]

def part2(data, invalidNumber):
	for i in range(len(data)-1):
		for j in range(i+1, len(data)):
			if abs(i-j) >= 2 and sum(data[i:j]) == invalidNumber:
				#print(f"data[{i}:{j}] Sum: {sum(data[i:j])} Result:{min(data[i:j])+max(data[i:j])}")
				print("Part 2:", min(data[i:j])+max(data[i:j]))
				return

if __name__ == "__main__":
	data = readFile("input.txt")

	invalidNumber = findInvalidNumber(data)
	print("Part 1:", invalidNumber)
	part2(data, invalidNumber)