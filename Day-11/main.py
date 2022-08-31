import copy
from pprint import pprint

def readFile(filename):
	with open(filename, "r") as file:
		return list(map(lambda x: list(x.strip("\n")), file.readlines()))

def checkVectorSimple(layout, vx, vy, x, y):
	x -= vx
	y -= vy
	if x >= 0 and y >= 0 and y < len(layout) and x < len(layout[0]):
		return layout[y][x] == "#"
	return False

def checkVectorAdvanced(layout, vx, vy, x, y):
	x += vx
	y += vy
	while 0<=y and 0<=x and y<len(layout) and x<len(layout[0]):
		if layout[y][x] == "#":
			return True
		elif layout[y][x] == "L": #Blocking view
			return False
		x += vx
		y += vy
	return False

def countOccupiedAdjacent(layout,x,y,advanced=False):
	occupiedAdjacent = 0
	vectors = ( (1,0),(0,1),(-1,0),(0,-1), (1,1),(-1,-1),(1,-1),(-1,1) )

	for vx,vy in vectors:
		if advanced:
			occupiedAdjacent += checkVectorAdvanced(layout, vx, vy, x, y)
		else:
			occupiedAdjacent += checkVectorSimple(layout, vx, vy, x, y)
	return occupiedAdjacent

def simulateStep(layout, advanced=False):
	#Because the list internally contains string objects a simple copy is not enough
	out = copy.deepcopy(layout)

	if advanced:
		minOccupied = 5
	else:
		minOccupied = 4

	changedSomething = False
	for y in range(len(layout)):
		for x in range(len(layout[y])):
			occupiedAdjacent = countOccupiedAdjacent(layout, x, y, advanced=advanced)
			if layout[y][x] == "L" and occupiedAdjacent == 0: # Empty
				out[y][x] = "#" # Becomes occupied
				changedSomething = True
			elif layout[y][x] == "#" and minOccupied <= occupiedAdjacent: # Occupied
				out[y][x] = "L" # Becomes empty
				changedSomething = True
	if changedSomething:
		return out
	else:
		return None

def totalOccupied(layout):
	totalOccupied = 0
	for y in range(len(layout)):
		totalOccupied += layout[y].count("#")
	return totalOccupied

def simulate(layout, advanced=False):
	counter = 1
	newLayout = simulateStep(layout, advanced=advanced)
	while newLayout != None:
		layout = newLayout
		newLayout = simulateStep(layout, advanced=advanced)
		counter += 1
	print(f"Stabilized after {counter} turns")
	return totalOccupied(layout)

if __name__ == "__main__":
	layout = readFile("input.txt")
	print("Part 1:", simulate(layout, advanced=False))
	print("Part 2:", simulate(layout, advanced=True))