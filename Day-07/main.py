import re
from pprint import pprint

class Vertex:
	def __init__(self, id):
		self.id = id
		self.mark = False

class Edge:
	def __init__(self, vertex1, vertex2, weight=None):
		self.weight = weight
		self.vertex1 = vertex1
		self.vertex2 = vertex2

class Graph:
	def __init__(self):
		self.vertices = set()
		self.edges = set()

		# This graph implementation has a feature that can interpret the edges
		# as if the graph would be undirected or directed where for a directed graph
		# the nodes of the edge can be swapped (left,right mode)
		self.edgeMode = "both" # left,right,both 
	def getVertex(self, id):
		for vertex in self.vertices:
			if vertex.id == id:
				return vertex
	def addVertex(self, vertex):
		self.vertices.add(vertex)
	def addEdge(self, edge):
		self.edges.add(edge)
	def setAllVertexMarks(self, value):
		for vertex in self.vertices:
			vertex.mark = value
	def getNeighbours(self, vertex):
		neighbours = []
		for edge in self.edges:
			if self.edgeMode == "left":
				if edge.vertex2 == vertex:
					neighbours.append(edge.vertex1)
			elif self.edgeMode == "right":
				if edge.vertex1 == vertex:
					neighbours.append(edge.vertex2)
			elif self.edgeMode == "both":
				if edge.vertex1 == vertex or edge.vertex2 == vertex:
					neighbours.append(edge.vertex2)
		return neighbours
	
	def getEdge(self, vertex1, vertex2):
		for edge in self.edges:
			if self.edgeMode == "left":
				if edge.vertex1 == vertex2 and edge.vertex2 == vertex1:
					return edge
			elif self.edgeMode == "right":
				if edge.vertex1 == vertex1 and edge.vertex2 == vertex2:
					return edge
			elif self.edgeMode == "both":
				condition1 = edge.vertex1 == vertex2 and edge.vertex2 == vertex1
				condition2 = edge.vertex1 == vertex1 and edge.vertex2 == vertex2
				if condition1 or condition2:
					return edge

def readFile(filename):
	with open(filename, "r") as file:
		lines = file.readlines()

	pattern = re.compile("^(\\w+ \\w+) bags contain (.+)\\.$")
	graph = Graph()
	for line in lines:
		inputBag, temp = re.search(pattern, line.strip("\n")).groups()

		inVertex = graph.getVertex(inputBag)
		if not inVertex: # Create Vertex if not already existing
			inVertex = Vertex(inputBag)
			graph.addVertex(inVertex)

		for entry in temp.split(","):
			if "no other" not in entry:
				amount, outBag = re.search("(\\d+) (\\w+ \\w+) bags?", entry).groups()

				outVertex = graph.getVertex(outBag)
				if not outVertex: # Create Vertex if not already existing
					outVertex = Vertex(outBag)
					graph.addVertex(outVertex)

				graph.addEdge(Edge(inVertex, outVertex, int(amount)))
	return graph

# Basically modified depth-search, no need for vertex marking because graph is acyclic
def visualizeGraphRecursive(graph, currentVertex, identation):
	if len(graph.getNeighbours(currentVertex)) > 0:
		print("│"*identation + "├┬" + currentVertex.id)
	else:
		print("│"*identation + "├─" + currentVertex.id)
	for neighbour in graph.getNeighbours(currentVertex):
		visualizeGraphRecursive(graph, neighbour, identation+1) # Recursion
		#count += graph.getEdge(currentVertex, neighbour).weight * subAmount

def visualizeGraph(graph, edgeMode):
	if edgeMode == "left" or edgeMode == "right":
		graph.edgeMode = edgeMode
		print("Edge-Mode:", edgeMode)
		startVertex = graph.getVertex("shiny gold")
		visualizeGraphRecursive(graph, startVertex, 0)
	else:
		print(
			"Please select either left or right as edge mode both-mode results in "+
			"Stackoverflow because the rests of the functions where designed for an acyclic graph"
		)

# Basically modified broad search, no need for vertex marking because graph is acyclic
def part1(graph):
	graph.edgeMode = "left"
	startVertex = graph.getVertex("shiny gold")
	parentVertices = set()
	q = [startVertex] # Dequeue
	while q != []: # While q not empty
		current = q.pop()
		parentVertices.add(current)
		for neighbour in graph.getNeighbours(current):
			q.append(neighbour)

	print("Part 1:", len(parentVertices)-1) # The startVertex does not count


# Basically modified depth-search, no need for vertex marking because graph is acyclic
def part2Recursion(graph, currentVertex):
	count = 1
	for neighbour in graph.getNeighbours(currentVertex):
		subAmount = part2Recursion(graph, neighbour) # Recursion
		count += graph.getEdge(currentVertex, neighbour).weight * subAmount
	return count

def part2(graph):
	graph.edgeMode = "right"
	startVertex = graph.getVertex("shiny gold")
	count = part2Recursion(graph, startVertex)-1 # The startVertex does not count
	print("Part 2:", count)
		
if __name__ == "__main__":
	graph = readFile("input.txt")
	
	#visualizeGraph(graph, "left")
	#print("\n\n\n\n\n")
	#visualizeGraph(graph, "right")

	print("Graph Stats:", len(graph.vertices), "Vertices and", len(graph.edges), "Edges")
	part1(graph)
	part2(graph)