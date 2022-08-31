from pprint import pprint
from functools import reduce

def readData(filename):
	with open(filename, "r") as file:
		lines = file.readlines()
	timestamp = int(lines[0].strip("\n"))
	ids = []
	for i in lines[1].strip("\n").split(","):
		if i == "x":
			ids.append(-1) # Use -1 instead of x
		else:
			ids.append(int(i))
	return timestamp, ids

def part1(timestamp, ids):
	ids = list(filter(lambda x: x != -1, ids))
	x = list(map(lambda x: x-(timestamp%x), ids))

	waitingDuration = min(x)
	minBusId = ids[x.index(waitingDuration)]
	print("Min-Bus-ID:", minBusId, " Waiting-Duration:", waitingDuration)
	print("Part 1:", minBusId*waitingDuration)

def mulInv(a, b):
	b0 = b
	x0 = 0
	x1 = 1
	if b == 1:
		return 1
	while a > 1:
		q = int(a / b)
		a, b = b, a % b
		x0, x1 = x1 - q * x0, x0
	if x1 < 0:
		x1 += b0
	return x1

def chineseRemainderTheorem(nArr, aArr):
	# https://rosettacode.org/wiki/Chinese_remainder_theorem
	mySum = 0
	prod = reduce(lambda a, b: a*b, nArr)
	for i in range(len(nArr)):
		p = int(prod / nArr[i])
		mySum += aArr[i] * mulInv(p, nArr[i]) * p
	return mySum % prod

def part2(ids):
	nArr = []
	aArr = []
	for i in range(len(ids)):
		if ids[i] != -1:
			nArr.append(ids[i])
			aArr.append(-i)
	result = chineseRemainderTheorem(nArr, aArr)

	print("Part 2:", result)

if __name__ == "__main__":
	timestamp, ids = readData("input.txt")
	part1(timestamp, ids)
	part2(ids)
	