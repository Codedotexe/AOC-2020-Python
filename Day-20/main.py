import re
import math
from collections import deque

class Edge:
	def __init__(self, edgeArray):
		self.checksum, self.flippedChecksum = self.calculateChecksums(edgeArray)
		self.adjacentEdges = set()
		self.adjacentTiles = set()
		self.isOuter = False
		
	def calculateChecksums(self, edgeArray):
		checksum = 0
		flippedChecksum = 0
		for i in range(len(edgeArray)):
			if edgeArray[i]:
				checksum += 2**i
			if edgeArray[len(edgeArray)-1-i]:
				flippedChecksum += 2**i
		return checksum, flippedChecksum

	def flip(self):
		self.checksum, self.flippedChecksum = self.flippedChecksum, self.checksum

	def edgeIsCompatible(self, edge):
		return edge.checksum == self.checksum or edge.checksum == self.flippedChecksum

class Tile:
	def __init__(self, tileArray, tileNumber):
		self.tileArray = tileArray
		self.tileNumber = tileNumber
		self.edges = self.determineEdges()
		self.rotation = 0
		self.hasVflipped = False
		self.hasHfliped = False
		self.isUsed = False # Needed for image.solve function
		self.isOuter = False

	def determineEdges(self):
		edgeArrayTop = []
		edgeArrayRight = []
		edgeArrayBottom = []
		edgeArrayLeft = []
		for i in range(len(self.tileArray)):
			edgeArrayTop.append(self.tileArray[0][i])
			edgeArrayRight.append(self.tileArray[i][len(self.tileArray)-1])
			edgeArrayBottom.append(self.tileArray[len(self.tileArray)-1][i])
			edgeArrayLeft.append(self.tileArray[i][0])

		return deque([Edge(edgeArrayTop), Edge(edgeArrayRight), 
			Edge(edgeArrayBottom), Edge(edgeArrayLeft)])

	def rotate(self, rot):
		self.rotation = (self.rotation + rot) % 4
		self.edges.rotate(rot % 4)	

	def vflip(self):
		self.hasVflipped = not self.hasVflipped
		self.edges[0].flip()
		self.edges[2].flip()
		self.edges[1], self.edges[3] = self.edges[3], self.edges[1]

	def hflip(self):
		self.hasHfliped = not self.hasHfliped
		self.edges[1].flip()
		self.edges[3].flip()
		self.edges[0], self.edges[2] = self.edges[2], self.edges[0]

	def transposeTileArray(self):
		for i in range(len(self.tileArray)):
			for j in range(i):
				self.tileArray[i][j], self.tileArray[j][i] = self.tileArray[j][i], self.tileArray[i][j]

	def rotateTileArray(self, n):
		n %= 4
		if n < 0: # -90 deg rotate
			for i in range(abs(n)):
				self.vflipTileArray()
				self.transposeTileArray()
		elif 0 < n: # 90 deg rotate
			for i in range(n):
				self.transposeTileArray()
				self.vflipTileArray()

	def vflipTileArray(self):
		for i in range(len(self.tileArray)):
			for j in range(int(len(self.tileArray)/2)):
				self.tileArray[i][j], self.tileArray[i][len(self.tileArray)-1-j] = self.tileArray[i][len(self.tileArray)-1-j], self.tileArray[i][j]

	def hflipTileArray(self):
		for i in range(int(len(self.tileArray)/2)):
			self.tileArray[i], self.tileArray[len(self.tileArray)-1-i] = self.tileArray[len(self.tileArray)-1-i], self.tileArray[i]

	def applyTileArrayTransformations(self):
		if self.rotation > 0:
			self.rotateTileArray(self.rotation)
			self.rotation = 0
		if self.hasVflipped:
			self.vflipTileArray()
			self.hasVflipped = False
		if self.hasHfliped:
			self.hflipTileArray()
			self.hasHfliped = False

	def print(self):
		for row in self.tileArray:
			line = ""
			for cell in row:
				if cell:
					line += "#"
				else:
					line += "."
			print(line)
	
	def removeBorder(self):
		self.tileArray.pop(0)
		self.tileArray.pop()
		for row in self.tileArray:
			row.pop(0)
			row.pop()
		self.edges = self.determineEdges()

	def countTruePixels(self):
		count = 0
		for row in self.tileArray:
			for cell in row:
				if cell:
					count += 1
		return count

class Image:
	def __init__(self, tiles):
		self.tiles = tiles
		self.fieldLength = int(math.sqrt(len(self.tiles)))
		self.field = []
		for i in range(self.fieldLength):
			self.field.append([None]*self.fieldLength)
		self.calculateAdjacentEdges()

		self.cornerTiles = self.determineCornerTiles()

	def calculateAdjacentEdges(self):
		for tileA in self.tiles:
			for tileB in self.tiles:
				if tileA is not tileB:
					for edgeA in tileA.edges:
						for edgeB in tileB.edges:
							if edgeA is not edgeB and edgeA.edgeIsCompatible(edgeB):
								edgeA.adjacentEdges.add(edgeB)
								edgeA.adjacentTiles.add(tileB)
								edgeB.adjacentEdges.add(edgeA)
								edgeB.adjacentTiles.add(tileA)

	def determineCornerTiles(self): # Find a corner tile
		cornerTiles = set()
		for tile in self.tiles:
			outerEdgesCount = 0
			for edge in tile.edges:
				if len(edge.adjacentEdges) == 0:
					edge.isOuter = True
					outerEdgesCount += 1	
			if outerEdgesCount == 2:
				tile.isOuter = True
				cornerTiles.add(tile)
			elif outerEdgesCount > 2:
				print("ERROR: Tile has more than two outer tiles")
				exit(1)
		return cornerTiles

	def findEmptyLocation(self):
		for i in range(self.fieldLength):
			for j in range(self.fieldLength):
				if self.field[i][j] == None:
					return (i, j)
		return (-1, -1)

	def checkLocationIsSafe(self, row, col, tile):
		if 0 <= row-1 and self.field[row-1][col] and self.field[row-1][col].edges[2] not in tile.edges[0].adjacentEdges: # Top
			return False

		if 0 <= col-1 and self.field[row][col-1] and self.field[row][col-1].edges[1] not in tile.edges[3].adjacentEdges: # Left
			return False

		if row+1 < len(self.field) and self.field[row+1][col] and self.field[row+1][col].edges[0] not in tile.edges[2].adjacentEdges: # Bottom
			return False

		if col+1 < len(self.field) and self.field[row][col+1] and self.field[row][col+1].edges[2] not in tile.edges[1].adjacentEdges: # Right
			return False
		
		return True


	def solve(self): # Backtracking
		row, col = self.findEmptyLocation()
		if row == -1:
			return True

		tilesSet = set()
		if (row == 0 or row == self.fieldLength-1) and (col == 0 or col == self.fieldLength-1):
			tilesSet.update(self.cornerTiles)
		else:
			if 0 <= row-1 and self.field[row-1][col]: # Top
				tilesSet.update(self.field[row-1][col].edges[2].adjacentTiles)

			if 0 <= col-1 and self.field[row][col-1]: # Left
				tilesSet.update(self.field[row][col-1].edges[1].adjacentTiles)

			if row+1 < len(self.field) and self.field[row+1][col]: # Bottom
				tilesSet.update(self.field[row+1][col].edges[0].adjacentTiles)

			if col+1 < len(self.field) and self.field[row][col+1]: # Right
				tilesSet.update(self.field[row][col+1].edges[2].adjacentTiles)

		#for tile in self.tiles:
		for tile in tilesSet:
			if tile.isUsed == False:
				self.field[row][col] = tile # make tentative assignment
				tile.isUsed = True

				for rot in range(4):
					if self.checkLocationIsSafe(row, col, tile) and self.solve():
						return True

					tile.vflip()
					if self.checkLocationIsSafe(row, col, tile) and self.solve():
						return True
					tile.vflip()

					tile.hflip()
					if self.checkLocationIsSafe(row, col, tile) and self.solve():
						return True
					tile.hflip()			

					tile.rotate(1)

				self.field[row][col] = None
				tile.isUsed = False
		return False # this triggers backtracking

	def constructCompeteField(self):
		for row in self.field:
			for cell in row:
				if cell:
					cell.applyTileArrayTransformations()

		completeField = []
		cellTileArrayLength = len(self.field[0][0].tileArray)
		for row in self.field:
			for i in range(cellTileArrayLength):
				fieldRow = []
				for cell in row:
					if cell:
						fieldRow += cell.tileArray[i]
				completeField.append(fieldRow)
		return Tile(completeField, -1)

	def multiplyCornerIds(self):
		if self.findEmptyLocation()[0] == -1:
			x = self.field[0][0].tileNumber 
			x *= self.field[self.fieldLength-1][0].tileNumber
			x *= self.field[0][self.fieldLength-1].tileNumber
			x *= self.field[self.fieldLength-1][self.fieldLength-1].tileNumber
			return x
		else:
			return -1
	
	def removeBorders(self):
		for tile in self.tiles:
			tile.removeBorder()

def readData(filename):
	with open(filename, "r") as file:
		data = file.read().split("\n\n")

	tiles = []
	for entry in data:
		lines = entry.split("\n")
		if len(lines) == 11:
			num = int(re.search("Tile (\\d+):", lines[0]).groups()[0])
			field = []
			for i in lines[1:]:
				temp = []
				for j in i:
					temp.append(j == "#")
				field.append(temp)
			tiles.append(Tile(field, num))
	return tiles

def searchSeamonsterHelper(tileArrayRow, monsterRow):
	maxIndex = len(tileArrayRow) - (len(monsterRow)-1)

	for i in range(maxIndex):
		valid = True

		for j in range(len(monsterRow)):
			if monsterRow[j] == '#' and tileArrayRow[i+j] == False:
				valid = False
		
		if valid:
			return True
	return False

def searchSeamonster(tile):
	monster = (
		'                  # ',
		'#    ##    ##    ###',
		' #  #  #  #  #  #   '
	)
	monsterCount = 0

	for i in range(len(tile.tileArray)-2):
		valid = True

		for j in range(len(monster)):
			if not searchSeamonsterHelper(tile.tileArray[i], monster[j]):
				valid = False
				break
		
		if valid:
			monsterCount += 1
				
	return monsterCount

def findSeamonsters(tile):
	monsterCount = 0
	for i in range(4):
		if searchSeamonster(completeField) > 0:
			monsterCount += searchSeamonster(completeField)

		completeField.hflipTileArray()
		if searchSeamonster(completeField) > 0:
			monsterCount += searchSeamonster(completeField)
		completeField.hflipTileArray()

		completeField.vflipTileArray()
		if searchSeamonster(completeField) > 0:
			monsterCount += searchSeamonster(completeField)
		completeField.vflipTileArray()

		completeField.rotateTileArray(1)
	return monsterCount


def pickleSave(image, filename):
	import pickle
	for tile in image.tiles: # Remove edges because cyclic reference problems
		tile.edges = None
	with open(filename, "wb") as file:
		pickle.dump(image, file)

def pickleLoad(filename):
	import pickle
	with open(filename, "rb") as file:
		return pickle.load(file)

if __name__ == "__main__":
	tiles = readData("input.txt")
	image = Image(tiles)
	image.solve()

	# Part 1
	print("Part 1:", image.multiplyCornerIds())

	# Part 2
	image.removeBorders()
	completeField = image.constructCompeteField()
	monsterCount = findSeamonsters(completeField)
	result = completeField.countTruePixels() - (monsterCount * 15) # 15 is number of true pixels in monster
	print("Part 2:", result)
