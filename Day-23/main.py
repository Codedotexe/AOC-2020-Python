import copy

class Node:
	def __init__(self, value):
		self.value = value
		self.next = None

class CircularLinkedList:
	# https://www.baeldung.com/java-circular-linked-list
	def __init__(self):
		self.head = None
		self.tail = None
		self.size = 0
		self.lookup = dict()
	
	def insertEnd(self, newNode):
		if newNode == None:
			raise AttributeError()

		if self.head == None:
			self.head = newNode
		else:
			self.tail.next = newNode
		self.tail = newNode
		self.tail.next = self.head
		self.size += 1
		self.lookup[newNode.value] = newNode
	
	def insertAfter(self, targetNode, newNode):
		if newNode == None or targetNode == None:
			raise AttributeError()
		if targetNode == self.tail:
			self.insertEnd(newNode)
		else:
			self.size += 1
			self.lookup[newNode.value] = newNode
			temp = targetNode.next
			targetNode.next = newNode
			newNode.next = temp

	def delete(self, targetNode):
		if targetNode == None:
			raise AttributeError()

		self.size -= 1
		del self.lookup[targetNode.value]
		curNode = self.head
		if self.head == None:
			return False # Deleting not possible
	
		doWhile = True
		while curNode != self.head or doWhile:
			doWhile = False
			nextNode = curNode.next
			if nextNode == targetNode:
				if self.tail == self.head: # List has only one element (should never be reached)
					self.head = None
					self.tail = None
				else:
					curNode.next = nextNode.next
					if self.head == nextNode: # Deleting the head
						self.head = self.head.next
					if self.tail == nextNode: # Deleting the tail
						self.tail = curNode
				break
			curNode = nextNode

		return True # Finished delteting

	def rotate(self, amount):
		for i in range(amount):
			self.head = self.head.next
			self.tail = self.tail.next
	
	def rotateTo(self, targetNode):
		temp = self.head
		while self.head != targetNode:
			self.head = self.head.next
			self.tail = self.tail.next
			if self.head == temp: # Did one full revolution
				break
	
	def __iter__(self):
		self._iterCur = self.head
		return self

	def __next__(self):
		if self._iterCur == None:
			raise StopIteration
		node = self._iterCur
		self._iterCur = self._iterCur.next
		if self._iterCur == self.head:
			self._iterCur = None
		return node

	def __str__(self):
		return '[' + ",".join(map(lambda x: str(x.value), self)) + ']'
	
	def count(self):
		i = 0
		for j in self:
			i += 1
		return i 

def readFile(filePath):
	with open(filePath, "r") as file:
		cups = CircularLinkedList()
		for i in file.read().strip('\n'):
			cups.insertEnd(Node(int(i)))
		return cups

def doMoves(cups, amount):
	for t in range(amount):
		threeCups = (cups.head.next, cups.head.next.next, cups.head.next.next.next)

		x = cups.head.value 
		destCup = threeCups[0] # To simulate a do-while loop
		while destCup == threeCups[0] or destCup == threeCups[1] or destCup == threeCups[2]:
			x -= 1
			if x < 1:
				x = cups.size  # Because of the three deleted
			destCup = cups.lookup[x]


		temp = destCup
		for i in threeCups:
			cups.delete(i)
			cups.insertAfter(temp, i)
			temp = i 

		# Rotate the list
		cups.rotate(1)

def part1(cups):
	cupsMod = copy.deepcopy(cups)
	doMoves(cupsMod, 100)
	cupsMod.rotateTo(cupsMod.lookup[1])

	result = "".join(map(lambda x: str(x.value), list(cupsMod)[1:]))
	print("Part 1:", result)

def part2(cups):
	cupsMod = copy.deepcopy(cups)
	for i in range(cupsMod.size, 1000000):
		cupsMod.insertEnd(Node(i+1))

	doMoves(cupsMod, 10000000)

	cupOne = cupsMod.lookup[1]
	result = cupOne.next.value * cupOne.next.next.value
	print("Part 2:", cupOne.next.value, "*", cupOne.next.next.value, "=", result)

if __name__ == "__main__":
	#cups = readFile("input_test.txt")
	cups = readFile("input.txt")

	part1(cups)
	part2(cups)

	# Note: for some reason a copy.deepcopy is needed as simple copy.copy does not work
	# I have no idea why that is, when using a simple copy the cupsList is missing a few nodes
	# after adding the million cups add the start of part 2. The deepcopy may also have unwanted
	# effects, maybe the hashtable of the list now has pointers to the old elements and not the new cloned
	# ones? But somehow is still works so I ignored it for now. Alternative to cloning would be to create the 
	# list for part 1 and part 2 from scratch from the puzzle input.

