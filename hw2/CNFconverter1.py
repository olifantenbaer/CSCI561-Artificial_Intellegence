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
        cnfList = deleteAndReturn(cnfList)
        return cnfList
    if cnfList[0] is "or":
        if orReturn(cnfList) is True:
            cnfList = deleteOrReturn(cnfList)
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
    length = len(cnfList)
    i = 1
    while i < length:
        if isinstance(cnfList[i],ListType) and cnfList[i][0] != "not":
            newList = cnfList[i][1:]
            newList.sort()
            cnfList[i] = ["or"]+newList
        i = i+1
    i = 1
    while i < length:
        j = i+1
        while j < length:
            if cnfList[i] == cnfList[j]:
                length = length - 1
                del cnfList[j]
            else:
                j = j + 1
        i = i + 1
    return cnfList

def deleteOrReturn(cnfList):
    newList = []
    for item in cnfList:
        if item not in newList:
            newList.append(item)
    if len(newList) == 2 and newList[0] == "or":
        return newList[1]
    return newList

def orReturn(cnfList):
    for i in range(1,len(cnfList)):
        if isVariable(cnfList[i]) is not True:
            return False
    return True

def isVariable(cnfList)	:
    if isinstance(cnfList,StringType) and len(cnfList) == 1:
        return True
    elif isinstance(cnfList,ListType) and cnfList[0] == "not" and isinstance(cnfList[1],StringType) and len(cnfList[1]) == 1:
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

#inputFile = open(sys.argv[2],"r")
inputFile = open("test.txt","r")
outputFile = open("sentences_CNF.txt","w")
sentenceNum = int(inputFile.readline())
print sentenceNum
for i in range(0,sentenceNum):
    cnfList = eval(inputFile.readline())
    cnfList = cnfConverter(cnfList)
    outputFile.write(repr(cnfList))
    outputFile.write("\n")
    print i



