def transform(inputNumber, loopSize):
	val = 1
	for i in range(loopSize):
		val *= inputNumber
		val %=  20201227
	return val

def bruteForceLoopSize(inputNumber, outputNumber):
	i = 1
	val = 1
	while True:
		val *= inputNumber
		val %=  20201227
		if val == outputNumber:
			return i
		i += 1

def part1(cardPubKey, doorPubKey):
	cardLoopSize = bruteForceLoopSize(7, cardPubKey)
	print("Card Loop Size", cardLoopSize)
	encryptionKey = transform(doorPubKey, cardLoopSize)
	print("Encryption Key", encryptionKey)

if __name__ == "__main__":
	cardPubKey = 8987316
	doorPubKey = 14681524
	part1(cardPubKey, doorPubKey)