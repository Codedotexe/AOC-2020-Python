from copy import copy
import re

def readFile(filePath):
	dirLookup = {
		"ne": (1,0,-1), "e": (1,-1,-0),"se": (0,-1,1), 
		"sw": (-1,0,1),"w": (-1,1,0), "nw": (0,1,-1)
	}
	pattern = re.compile("e|se|sw|w|nw|ne")

	# Extract instructions
	tileInstructions = []
	with open(filePath, "r") as file:
		for line in file.readlines():
			matches = re.findall(pattern, line.strip("\n"))
			tileInstructions.append(list(map(lambda x: dirLookup[x], matches)))
	return tileInstructions

def Vec3Add(vec1, vec2):
	return (vec1[0]+vec2[0],vec1[1]+vec2[1],vec1[2]+vec2[2])

def tilePosFromInstructions(instructions):
	pos = [0,0,0]
	for translation in instructions:
		pos = Vec3Add(pos, translation)
	return tuple(pos)

def genCubeMap(instructions):
	# Generate the hex map in cubes representation from the instructions
	cubeMap = dict()#{(0,0,0): 01}
	for instructions in tileInstructions:
		pos = tilePosFromInstructions(instructions)
		if pos not in cubeMap:
			cubeMap[pos] = 1 # 0=White 1=Black
		else:
			cubeMap[pos] = (cubeMap[pos] + 1) % 2 # Flip tile color
	return cubeMap



def adjacentBlackTiles(cubeMap, pos, cubeMapMod):
	translations = ((1,0,-1),(1,-1,-0),(0,-1,1),(-1,0,1),(-1,1,0),(0,1,-1))
	blackTiles = 0
	for translation in translations:
		neighbourPos = Vec3Add(pos, translation)
		if neighbourPos in cubeMap:
			if cubeMap[neighbourPos] == 1: # If black
				blackTiles += 1
		else:
			cubeMapMod[neighbourPos] = 0 # New Tile is white 
	return blackTiles

def fixEdges(cubeMap):
	# Add the (white) outer border tiles of the map to the map so they can be accessed in part2
	translations = ((1,0,-1),(1,-1,-0),(0,-1,1),(-1,0,1),(-1,1,0),(0,1,-1))
	newTiles = []
	for pos,val in cubeMap.items():
		for translation in translations:
			neighbourPos = Vec3Add(pos, translation)
			if neighbourPos not in cubeMap:
				newTiles.append(neighbourPos)
	for newTile in newTiles:
		cubeMap[newTile] = 0 # New Tile is white 

def gameOfLife(cubeMap, iterations):
	fixEdges(cubeMap)
	for t in range(iterations):
		#print(f"T={t}: {sum(cubeMap.values())}")
		cubeMapMod = copy(cubeMap)
		for pos, color in cubeMap.items():
			adjcantBlackTiles = adjacentBlackTiles(cubeMap, pos, cubeMapMod)
			if color == 1 and (adjcantBlackTiles == 0 or adjcantBlackTiles > 2):
					cubeMapMod[pos] = 0
			elif color == 0 and adjcantBlackTiles == 2:
					cubeMapMod[pos] = 1
		cubeMap = cubeMapMod
	return cubeMap

if __name__ == "__main__":
	tileInstructions = readFile("input.txt")
	cubeMap = genCubeMap(tileInstructions)
	print("Part 1:", sum(cubeMap.values()))
	print("Part 2:", sum(gameOfLife(cubeMap, 100).values()))
