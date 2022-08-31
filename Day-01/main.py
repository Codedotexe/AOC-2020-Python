def readFile(filename):
	with open(filename, "r") as file:
		return list(map(lambda x: int(x), file.readlines()))

def part1(numbers):
	for i in numbers:
		for j in numbers:
			if i!=j and i+j==2020:
				return i*j

def part2(numbers):
	for i in numbers:
		for j in numbers:
			for k in numbers:
				if i!=j and j!=k and i+j+k==2020:
					return i*j*k

if __name__ == "__main__":
	numbers = readFile("input.txt")
	print("Part 1:", part1(numbers))
	print("Part 2:", part2(numbers))