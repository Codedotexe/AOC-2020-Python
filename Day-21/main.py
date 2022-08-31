from pprint import pprint

class Food:
	def __init__(self, ingredients, allergens):
		self.ingredients = ingredients
		self.allergens = allergens

def readFile(filename):
	with open(filename, "r") as file:
		lines = file.readlines()

	foods = []
	allAllergens = set()
	allIngredients = set()
	for line in lines:
		line = line.strip("\n")
		pre,sep,after = line.partition("(contains ")
		ingredients = set(pre.strip(" ").split(" "))
		allergens = set(after.strip(")").strip(" ").split(", "))
		allAllergens.update(allergens)
		allIngredients.update(ingredients)
		foods.append(Food(ingredients, allergens))
	
	return foods, allIngredients, allAllergens

def createAllergensMap(foods, ingredients, allergens):
	allergensMap = dict()
	for food in foods:
		for foodAllergen in food.allergens:
			ingredientsSet = set(food.ingredients)
			createAllergensMapHelper(foods, ingredientsSet, foodAllergen)
			allergensMap[foodAllergen] = ingredientsSet

	return allergensMap

def createAllergensMapHelper(foods, ingredientsSet, targetAllergen):
	for food in foods:
		if targetAllergen in food.allergens:
			ingredientsSet.intersection_update(food.ingredients)

def filterAllergensMap(allergensMap):
	for key, values in allergensMap.items():
		if len(values) == 1:
			ingredient = next(iter(values))
			for key2 in allergensMap.keys():
				if key != key2 and ingredient in allergensMap[key2]:
					allergensMap[key2].remove(ingredient)
					return True
	return False

if __name__ == "__main__":
	#foods, ingredients, allergens = readFile("input_test.txt")
	foods, ingredients, allergens = readFile("input.txt")

	allergensMap = createAllergensMap(foods, ingredients, allergens)

	modified = True
	while modified:
		modified = filterAllergensMap(allergensMap)

	for key in allergens: # Transform single element set to simple attribute
		allergensMap[key] = allergensMap[key].pop()

	# Part 1
	safeIngredients = ingredients.difference(allergensMap.values())
	counter = 0
	for food in foods:
		counter += len(safeIngredients.intersection(food.ingredients))
	print("Part 1:", counter)

	# Part 2
	allergensMapItems = list(allergensMap.items())
	allergensMapItems.sort(key=lambda x: x[0])
	unsafeIngredients = map(lambda x: x[1], allergensMapItems)
	unsafeIngredientsString = ",".join(unsafeIngredients)
	print("Part 2:", unsafeIngredientsString)

