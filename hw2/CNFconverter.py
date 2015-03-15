import sys
import pdb
from types import*
def cnfConverter(cnfList):
	if isVariable(cnfList) is True:
		return cnfList
	if(cnfList[0] is "iff"):
		cnfList = iff(cnfList)
		cnfList = cnfConverter(cnfList)
		return cnfList
	if(cnfList[0] is "implies"):
		cnfList = implies(cnfList)
		cnfList = cnfConverter(cnfList)
		return cnfList
	if(cnfList[0] is "not"):
		if(type(cnfList[1]) is StringType):
			return cnfList
		if(cnfList[1][0] is "not"):
			cnfList = not_Not(cnfList)
			return cnfConverter(cnfList)
		if(cnfList[1][0] is "and"):
			cnfList = not_And(cnfList)
			return cnfConverter(cnfList)
		if(cnfList[1][0] is "or"):
			cnfList = not_Or(cnfList)
			return cnfConverter(cnfList)
		if(cnfList[1][0] is "implies"):
			cnfList[1] = cnfConverter(cnfList[1])
			cnfList = cnfConverter(cnfList)
			return cnfList
		if(cnfList[1][0] is "iff"):
			cnfList[1] = cnfConverter(cnfList[1])
			cnfList = cnfConverter(cnfList)
			return cnfList
	if(cnfList[0] is "and"):
		i = 1
		while (i < len(cnfList)):
			cnfList[i] = cnfConverter(cnfList[i])
			i = i + 1 
		cnfList = mergeAnd(cnfList)
		return cnfList
	if(cnfList[0] is "or"):
		if orReturn(cnfList) is True:
			return cnfList
		i = 1
		while i < len(cnfList):
			cnfList[i] = cnfConverter(cnfList[i])
			i = i + 1
		cnfList = mergeOr(cnfList)
		cnfList = orDistribution(cnfList)	
		cnfList = cnfConverter(cnfList)
		return cnfList

def deleteAndReturn(cnfList):
	i_max = len(cnfList)
	i = 0
	while i < i_max:
		j = i + 1
		while j < i_max
			
		

def deleteOrReturn(cnfList):
	newList = []
	for item in cnfList:
		if item not in cnfList:
			newList.append(item)
	return newList

	
def orReturn(cnfList):
	for i in range(1,len(cnfList)):
		if isVariable(cnfList[i]) is not True:
			return False
	return True
	
def isVariable(cnfList)	:
	if type(cnfList) is StringType:
		return True
	elif cnfList[0] is "not":
		if type(cnfList[1]) is StringType:
			return True
		else:
			return False
			
def mergeOr(cnfList):
	i = 1
	maxL = len(cnfList)
	while i < maxL:
		if(type(cnfList[i]) is not StringType):
			if cnfList[i][0] is "or":
				for j in range(1,len(cnfList[i])):
					cnfList.append(cnfList[i][j])
				cnfList.pop(i)
				maxL = maxL - 1
			else:
				i = i + 1
		else:
			i = i + 1
	return cnfList

def orDistribution(cnfList):
	for k in range(1,len(cnfList)):
		if(type(cnfList[k]) is not StringType):
			if(cnfList[k][0] is "and"):
				item = cnfList[k][:]
				cnfList.pop(k)
				newCnfList = ["and"]
				for j in range(1,len(item)):
					newItem = cnfList[:]
					newItem.append(item[j])
					newCnfList.append(newItem)
				cnfList = newCnfList
				break
	return cnfList	

def mergeAnd(cnfList):
	i = 1
	maxL = len(cnfList)
	while i < maxL:
		if(type(cnfList[i]) is not StringType):
			if cnfList[i][0] is "and":
				for j in range(1,len(cnfList[i])):
					cnfList.append(cnfList[i][j])
				cnfList.pop(i)
				maxL = maxL - 1
			else:
				i = i + 1
		else:
			i = i + 1
	return cnfList
	
def iff(cnfList):
	cnfList = ["or",["and",cnfList[1],cnfList[2]],["and",["not",cnfList[1]],["not",cnfList[2]]]]
	return cnfList
	
def implies(cnfList):
	cnfList = ["or",["not",cnfList[1]],cnfList[2]]
	return cnfList
	
def not_Not(cnfList):
	cnfList = cnfList[1][1]
	return cnfList
	
def not_And(cnfList):
	i = 1
	for item in cnfList[1]:
		if(item is cnfList[1][0]):
			cnfList[1][0] = "or"
		else:
			cnfList[1][i] = ["not",item]
			i = i + 1
	cnfList = cnfList[1]
	return cnfList

def not_Or(cnfList):
	i = 1
	for item in cnfList[1]:
		if(item is cnfList[1][0]):
			cnfList[1][0] = "and"
		else:
			cnfList[1][i] = ["not",item]
			i = i + 1
	cnfList = cnfList[1]
	return cnfList
	
	
file = open("test.txt")
sentenceNum = int(file.readline())
for i in range(0,sentenceNum):
	cnf = file.readline()
	pdb.set_trace()
	cnfList = eval(cnf)
	print cnfList
	# pdb.set_trace()
	ca = cnfConverter(cnfList)
	# cnfList = mergeAnd(cnfList)
	# cnfList = orDistribution(cnfList)

	print ca


