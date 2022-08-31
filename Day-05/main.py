def readFile(filename):
	with open(filename, "r") as file:
		return file.read().split("\n")

def decodeRow(rowString):
	lowerBound = 0
	upperBound = 127
	for i in rowString:
		if i == "F": #lower
			upperBound = int(upperBound-((upperBound-lowerBound)/2))
		else: #upper
			lowerBound = int(lowerBound+((upperBound-lowerBound)/2))+1
	return lowerBound

def decodeColumn(columnString):
	lowerBound = 0
	upperBound = 7
	for i in columnString:
		if i == "L": #lower
			upperBound = int(upperBound-((upperBound-lowerBound)/2))
		else: #upper
			lowerBound = int(lowerBound+((upperBound-lowerBound)/2))+1
	return lowerBound

def solve(data):
	seatIDs = []
	for entry in data:
		row = decodeRow(entry[:7])
		column = decodeColumn(entry[-3:])
		seatID = row*8+column
		seatIDs.append(seatID)
	seatIDs.sort()

	print("Part 1:", seatIDs[len(seatIDs)-1])

	for i in range(1, len(seatIDs)-2): # Rule out first and last seats
		if seatIDs[i]+1 != seatIDs[i+1]:
			print("Part 2:", seatIDs[i]+1)


if __name__ == "__main__":
	solve(readFile("input.txt"))