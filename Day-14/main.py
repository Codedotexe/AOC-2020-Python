import re

def readData(filename):
	with open(filename, "r") as file:
		return file.readlines()

def applyMaskValue(value, mask):
	binString = str(bin(value))[2:]
	binString = (len(mask)-len(binString))*"0" +binString
	resultBitStr = ""
	for i in range(len(binString)):
		if mask[i] == "0":
			resultBitStr += "0"
		elif mask[i] == "1":
			resultBitStr += "1"
		elif mask[i] == "X":
			resultBitStr += binString[i]
	return int(resultBitStr, 2)

def recursiveMaskFunction(addressBin, mask, resultBitStr="", i=0):
	if i >= len(mask):
		return [resultBitStr]

	addresses = []
	if mask[i] == "0":
		return recursiveMaskFunction(addressBin, mask, resultBitStr+addressBin[i], i+1)
	elif mask[i] == "1":
		return recursiveMaskFunction(addressBin, mask, resultBitStr+"1", i+1)
	elif mask[i] == "X": # Floating
		temp = recursiveMaskFunction(addressBin, mask, resultBitStr+"0", i+1)
		temp += recursiveMaskFunction(addressBin, mask, resultBitStr+"1", i+1)
		return temp

def applyMaskAddress(address, mask):
	binString = str(bin(address))[2:]
	binString = (len(mask)-len(binString))*"0" +binString
	addresses = recursiveMaskFunction(binString, mask)
	addresses = list(map(lambda x: int(x, 2), addresses))
	return addresses

def run(lines, advanced=False):
	mask, memCmd = None, None
	memory = dict()
	for line in lines:
		line = line.strip("\n")
		maskMatch = re.search("^mask = ([01X]+)$", line)
		if maskMatch:
			mask = list(maskMatch.groups()[0])
		memCmdMatch = re.search("^mem\\[(\\d+)\\] = (\\d+)$", line)
		if memCmdMatch:
			memCmd = (int(memCmdMatch.groups()[0]), int(memCmdMatch.groups()[1]))
			if advanced:
				for address in applyMaskAddress(memCmd[0], mask):
					memory[address] = memCmd[1]
			else:
				memory[memCmd[0]] = applyMaskValue(memCmd[1], mask)
	return sum(memory.values())
if __name__ == "__main__":
	lines = readData("input.txt")
	print("Part 1:", run(lines))
	print("Part 2:", run(lines, advanced=True))