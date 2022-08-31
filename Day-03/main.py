import math

def readFile(filename):
	output = [] # True means tree False means no tree
	with open(filename, "r") as file:
		temp = []
		for char in file.read():
			if char == "#":
				temp.append(True)
			elif char == ".":
				temp.append(False)
			elif char == "\n":
				output.append(temp)
				temp = []
	return output

def printField(field, shipPosHistory=[]):
	for i in range(len(field)):
		for j in range(len(field[i])):
			for k in shipPosHistory:
				if k == [j,i]:
					if field[i][j]:
						print("X", end="")
					else:
						print("O", end="")
			else:
				if field[i][j]:
					print("#", end="")
				else:
					print(".", end="")
		print() # Line Break

def navigate(field, slope):
	shipPos = [0,0] #[x,y]
	treeCounter = 0

	while shipPos[1] < len(field):
		if field[shipPos[1]][shipPos[0] % (len(field[0]))]: # Tree
			treeCounter += 1

		shipPos[0] += slope[0]
		shipPos[1] += slope[1]
	return treeCounter
	
def part1(field):
	print("Part 1:", navigate(field, (3,1)))

def part2(field):
	slopes = [[1,1],[3,1],[5,1],[7,1],[1,2]]
	factors = []
	for slope in slopes:
		factors.append(navigate(field, slope))
	print("Part 2:", math.prod(factors))

if __name__ == "__main__":
	field = readFile("input.txt")
	print("(w x h):",len(field[0]),"x",len(field))

	part1(field)
	part2(field)