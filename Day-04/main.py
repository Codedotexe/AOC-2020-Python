import re

def readFile(filename):
	with open(filename, "r") as file:
		data = file.read()

	output = []
	for i in data.split("\n\n"):
		i = i.replace("\n", " ")
		temp = dict()
		for j in i.split(" "):
			key, value = j.split(":")
			temp[key] = value
		output.append(temp)
	return output

def checkField(key, val):
	if key == "byr":
		if len(val) != 4 or int(val) < 1920 or int(val) > 2002:
			#print(key,"invalid:",val)
			return False
	elif key == "iyr":
		if len(val) != 4 or int(val) < 2010 or int(val) > 2020:
			#print(key,"invalid:",val)
			return False
	elif key == "eyr":
		if len(val) != 4 or int(val) < 2020 or int(val) > 2030:
			#print(key,"invalid:",val)
			return False
	elif key == "hgt":
		if re.match("^\\d+cm$", val):
			height = int(val.strip("cm"))
			if height < 150 or height > 193:
				#print(key,"invalid:",val)
				return False

		elif re.match("^\\d+in$", val):
			height = int(val.strip("in"))
			if height < 59 or height > 76:
				#print(key,"invalid:",val)
				return False
		else:
			#print(key,"invalid:",val)
			return False
	elif key == "hcl":
		if not re.match("^#[0-9a-f]{6}$", val):
		#if not re.match("^#([0-9]{6}|[a-f]{6})$", val):
			#print(key,"invalid:",val)
			return False
	elif key == "ecl":
		if not re.match("^(amb|blu|brn|gry|grn|hzl|oth)$", val):
			#print(key,"invalid:",val)
			return False
	elif key == "pid":
		if not re.match("^[0-9]{9}$", val):
			#print(key,"invalid:",val)
			return False
	return True

def checkData(data, checkContents):
	mandatoryFields = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]
	validEntries = 0
	for entry in data:
		ok = True

		for field in mandatoryFields: # Check if all fields are there
			if field not in entry.keys():
				ok = False

		if checkContents and ok: # Dont need to check contents when already failed
			for key, val in entry.items(): # Check field values more presisely
				if not checkField(key, val):
					ok = False
		if ok:
			validEntries += 1

	return validEntries


if __name__ == "__main__":
	data = readFile("input.txt")
	print("Part 1:", checkData(data, False))
	print("Part 2:", checkData(data, True))