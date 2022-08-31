def tokenize(string):
	out = []
	i = 0
	flag = False
	temp = ""
	for i in range(len(string)):
		if string[i].isdigit():
			temp += string[i]
		else:
			if temp != "":
				out.append(temp)
				temp = ""
			out.append(string[i])
	if temp != "":
		out.append(temp)
	return out

def infixToPostfix(infix, advanced): # Shunting-yard algorithm
	output = [] # Output Queue
	operators = [] # Operator Stack
	functionTokens = set(["+","*"])

	if advanced:
		precedences = {"+": 1, "*": 0} # Strich vor Punkt
	else:
		precedences = {"+": 0, "*": 0} # Gleichen Rang

	for token in tokenize(infix):
		#print(token,":", output, operators,end=" ")
		if token.isdigit():
			output.append(token)
		elif token in functionTokens:
			while operators != [] and (operators[-1] != "(" and precedences[token] <= precedences[operators[-1]]):
				output.append(operators.pop())
			operators.append(token)
		elif token == "(":
			operators.append(token)
		elif token == ")":
			while operators[-1] != "(":
				output.append(operators.pop())
			if operators[-1] == "(":
				operators.pop()
		#print("-->",output, operators)
	while operators != []:
		output.append(operators.pop())
	return output

def readData(filename):
	with open(filename, "r") as file:
		lines = file.readlines()
	return list(map(lambda x: x.strip("\n"), lines))

def evalPostfix(expression):
	functionTokens = set(["+","-","*","/"])
	stack = []
	for token in expression:
		if token not in functionTokens:
			stack.append(token)
		else:
			o1 = stack.pop()
			o2 = stack.pop()
			if token == "+":
				stack.append(int(o2)+int(o1))
			elif token == "*":
				stack.append(int(o2)*int(o1))
	return stack.pop()

def part1(infixEquations):
	outputSum = 0
	for infixEquation in infixEquations:
		postfixEquation = infixToPostfix(infixEquation, False)
		outputSum += evalPostfix(postfixEquation)
	print("Part1:", outputSum)

def part2(infixEquations):
	outputSum = 0
	for infixEquation in infixEquations:
		postfixEquation = infixToPostfix(infixEquation, True)
		outputSum += evalPostfix(postfixEquation)
	print("Part2:", outputSum)

if __name__ == "__main__":
	infixEquations = readData("input.txt")
	part1(infixEquations)
	part2(infixEquations)