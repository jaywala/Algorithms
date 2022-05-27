import time
import csv
import numpy as np
MAX_CALORIES = 2000

class Food(object):
	def __init__(self, n, v, w):
		self.name = n
		self.value = v
		self.calories = w
	def getValue(self):
		return self.value
	def getCost(self):
		return self.calories
	def density(self):
		return self.getValue()/self.getCost()
	def __str__(self):
		return self.name + ': <' + str(self.value)\
				 + ', ' + str(self.calories) + '>'

def buildMenu(names, values, calories):
	menu = []
	for i in range(len(values)):
		menu.append(Food(names[i], values[i],
						  calories[i]))
	return menu

def testMaxVal(foods, maxUnits, printItems = True):
	print('Allocate', maxUnits, 'calories')
	tic = time.time()
	val, taken = maxVal(foods, maxUnits)
	toc = time.time() - tic
	print('Total value of items taken =', val)
	if printItems:
		for item in taken:
			print('   ', item)
	print("time: %.5fs" % (toc))

def buildMenuFromCSV():
	menu = []
	with open('menu.csv', newline='') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',')
		for row in spamreader:
			try:
				menu.append(Food(row[0], int(row[1]),
								int(row[2])))
			except:
				continue
		return menu


def run():
	#example
	names = ['wine', 'beer', 'pizza', 'burger', 'fries',
			'cola', 'apple', 'donut', 'cake']
	values = [89,90,95,100,90,79,50,10]
	calories = [123,154,258,354,365,150,95,195]
	foods = buildMenu(names, values, calories)
	testMaxVal(foods, 750)

	#challenge
	menu = buildMenuFromCSV()
	testMaxVal(menu, MAX_CALORIES)


def maxVal(toConsider, avail):
	"""Assumes toConsider is a list of Food, avail a weight (number of calories)
	   Returns a tuple of the total value of a solution to the problem
	   and a list of Food that comprise the solution"""

	##################
	# YOUR CODE HERE #
	##################
	
	# Greedy solution The solution from this isn't correct but useful to estimate if dynamic programming solution is correct. 
	# Dynamic programming solution should atleast give value equal to higher than this solution
	# used = 0
	# value = 0
	# foodList = []
	# sortedFoodListByDensity = sorted(toConsider, key=lambda x: x.density(), reverse=True)
	# for food in sortedFoodListByDensity:
	#     # print(food, "density:", food.density())
	#     if food.calories + used <= avail:
	#         value = value + food.getValue()
	#         used = used + food.calories
	#         foodList.append(food)
	# print(f"{used = }")
	# print(f"{value = }")

	# print('toConsider')
	# for food in toConsider:
	# 	print(food)


	# sortedFoodList = sorted(toConsider, key=lambda x: x.getCost(), reverse=False)
	# Dynamic Prgrammic storage: Value Matrix is n foods by calaorie capacity
	valueMatrix = np.zeros((len(toConsider)+1,avail+1),dtype=int)

	for j in range(1,len(toConsider)+1):
		highest = 0
		food = toConsider[j-1]
		for i in range(1,avail+1):
			# Negative index case, hence use value from above row
			if (i-food.getCost() < 0):
				valueMatrix[j,i] = valueMatrix[j-1,i]
			# Case where we check both values for maximum
			else:
				valueMatrix[j,i] = max(valueMatrix[j-1,i], valueMatrix[j-1,i-food.getCost()] + food.getValue())

	# Start tracing sequence of decisions
	highestValue = valueMatrix[-1][-1]
	j = len(toConsider)
	i = avail
	DPfoodList = []
	while j != 0:
		if valueMatrix[j][i] != valueMatrix[j-1][i]:
			DPfoodList.append(toConsider[j-1])
			i -= toConsider[j-1].getCost()
		j -= 1

	# Test tracing sequence of steps is correct
	# sumValue = 0
	# for food in DPfoodList:
	# 	sumValue += food.getValue()
	# print(f"{valueMatrix[-1][-1] = }, {sumValue = }")
	# print('DPfoodList')
	# for food in DPfoodList:
	# 	print(food)

	# General Matrix Debugging
	# with np.printoptions(threshold=np.inf):
	#     print(valueMatrix)
	# print(valueMatrix)
	return (highestValue, DPfoodList)

if __name__ == '__main__':
	run()
