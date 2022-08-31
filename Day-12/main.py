import math
import re
from pprint import pprint

def readData(filename):
	with open(filename, "r") as file:
		lines = file.readlines()
	data = [] 
	pattern = re.compile("^([NSEWFLR])(\\d+)\n?$")
	for line in lines:
		match = re.search(pattern, line)
		if match:
			data.append([match.groups()[0], int(match.groups()[1])])
	return data

def cartesianToPolar(x,y):
	return math.sqrt(x*x + y*y), math.degrees(math.atan2(y,x))
def polarToCartesian(r,a):
	a = math.radians(a)
	return r*math.cos(a), r*math.sin(a)

class Waypoint:
	def __init__(self, x,y): # Init from cartesian
		self.distance, self.angle = cartesianToPolar(x,y)
	def moveByCartesian(self, x, y):
		wx,wy = polarToCartesian(self.distance, self.angle)
		self.distance, self.angle = cartesianToPolar(wx+x, wy+y)
	def moveNorth(self, value):
		self.moveByCartesian(0, -value)
	def moveSouth(self, value):
		self.moveByCartesian(0, value)
	def moveEast(self, value):
		self.moveByCartesian(value, 0)
	def moveWest(self, value):
		self.moveByCartesian(-value, 0)
	def turnRight(self, value):
		self.angle = (self.angle + value) % 360
	def turnLeft(self, value):
		self.turnRight(360 - value)
	def getPos(self):
		wx, wy = polarToCartesian(self.distance, self.angle)
		return round(wx), round(wy)

class Ferry:
	def __init__(self, pos=[0,0], heading=0, waypoint=None):
		self.pos = pos
		self.heading = heading # Degrees
		self.waypoint = waypoint
	def manhattenDistanceFromPos(self, px, py):
		return abs(self.pos[0] - px) + abs(self.pos[1] - py)
	def moveNorth(self, value):
		self.pos[1] -= value
	def moveSouth(self, value):
		self.pos[1] += value
	def moveEast(self, value):
		self.pos[0] += value
	def moveWest(self, value):
		self.pos[0] -= value
	def moveForward(self, value):
		self.pos[0] += int(value * math.cos(math.radians(self.heading)))
		self.pos[1] += int(value * math.sin(math.radians(self.heading)))
	def turnRight(self, value):
		self.heading = (self.heading + value) % 360
	def turnLeft(self, value):
		self.turnRight(360 - value)
	def moveToWaypoint(self, value):
		wx, wy = self.waypoint.getPos()
		self.pos[0] += wx * value
		self.pos[1] += wy * value

def part1(commands):
	ferry = Ferry()
	for command,value in commands:
		if command == "N":
			ferry.moveNorth(value)
		elif command == "E":
			ferry.moveEast(value)
		elif command == "S":
			ferry.moveSouth(value)
		elif command == "W":
			ferry.moveWest(value)
		elif command == "F":
			ferry.moveForward(value)
		elif command == "L":
			ferry.turnLeft(value)
		elif command == "R":
			ferry.turnRight(value)
	print(f"Part 1: Ferry position x:{ferry.pos[0]} y:{ferry.pos[1]}")
	print(f"Part 1: Manhatten Distance from (0,0): {ferry.manhattenDistanceFromPos(0,0)}")

def part2(commands):
	ferry = Ferry(waypoint=Waypoint(10,-1))
	for command,value in commands:
		if command == "N":
			ferry.waypoint.moveNorth(value)
		elif command == "E":
			ferry.waypoint.moveEast(value)
		elif command == "S":
			ferry.waypoint.moveSouth(value)
		elif command == "W":
			ferry.waypoint.moveWest(value)
		elif command == "F":
			ferry.moveToWaypoint(value)
		elif command == "L":
			ferry.waypoint.turnLeft(value)
		elif command == "R":
			ferry.waypoint.turnRight(value)
	print(f"Part 2: Ferry position x:{ferry.pos[0]} y:{ferry.pos[1]}")
	print(f"Part 2: Manhatten Distance from (0,0): {ferry.manhattenDistanceFromPos(0,0)}")

if __name__ == "__main__":
	commands = readData("input.txt")
	part1(commands)
	part2(commands)
