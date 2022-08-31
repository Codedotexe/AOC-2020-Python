from copy import copy
from pprint import pprint
import itertools

def readFile(filename):
	with open(filename, "r") as file:
		out = []
		line = []
		for char in file.read():
			if char == "#":
				line.append(True)
			elif char == ".":
				line.append(False)
			elif char =="\n":
				out.append(line)
				line = []
	return out

class PocketDimension():
	def __init__(self, dimensions, slice2D):
		self.dim = dimensions
		self.zeroVector = self.dim * [0]
		self.initFromSlice(slice2D)
		self.neighbourVecs = self.generateNeighbourVecs()

	def initFromSlice(self, slice2D):
		self.field = dict()
		for y in range(len(slice2D)):
			for x in range(len(slice2D[y])):
				pos = list(self.zeroVector)
				pos[0] = x
				pos[1] = y
				self.field[tuple(pos)] = slice2D[y][x]

	def generateNeighbourVecs(self):
		neighbourVecs = []
		zeroVector = tuple(self.zeroVector)
		for i in itertools.product((-1,0,1), repeat=self.dim):
			if i != zeroVector:
				neighbourVecs.append(i)
		return neighbourVecs
	
	def VecAdd(self, vec1, vec2):
		return map(sum, zip(vec1, vec2))

	def countAdjcantActive(self, pos, fieldMod):
		neighbourCount = 0
		for neighbourVec in self.neighbourVecs:
			newPoint = tuple(self.VecAdd(pos, neighbourVec))
			if newPoint in self.field:
				if self.field[newPoint]:
					neighbourCount += 1
			else:
				fieldMod[newPoint] = False
		return neighbourCount

	def fixEdges(self):
		newPoints = []
		for pos in self.field.keys():
			for neighbourVec in self.neighbourVecs:
				newPoint = tuple(self.VecAdd(pos, neighbourVec))
				if newPoint not in self.field:
					newPoints.append(newPoint)
		for newPoint in newPoints:
			self.field[newPoint] = False

	def simulate(self, iterations):
		self.fixEdges()
		for i in range(iterations):
			fieldMod = copy(self.field)
			for pos, state in self.field.items():
				adjacentActive = self.countAdjcantActive(pos, fieldMod)
				if state and (adjacentActive < 2 or adjacentActive > 3):
					fieldMod[pos] = False
				elif not state and adjacentActive == 3:
					fieldMod[pos] = True
			self.field = fieldMod

	def countActive(self):
		return sum(self.field.values())

if __name__ == "__main__":
	slice2D = readFile("input.txt")

	pocketDimension = PocketDimension(3, slice2D)
	pocketDimension.simulate(6)
	print("Part 1: Active Count:", pocketDimension.countActive())

	pocketDimension = PocketDimension(4, slice2D)
	pocketDimension.simulate(6)
	print("Part 2: Active Count:", pocketDimension.countActive())