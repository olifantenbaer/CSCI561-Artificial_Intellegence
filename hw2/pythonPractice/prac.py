from types import *
def isVariable(cnfList)	:
    if isinstance(cnfList,StringType) and len(cnfList) == 1:
        return True
    elif isinstance(cnfList,ListType) and cnfList[0] == "not" and isinstance(cnfList[1],StringType) and len(cnfList[1]) == 1:
        return True
    else:
        return False

def cnfIff(cnfList):
    if isVariable(cnfList):
        return cnfList
    if cnfList[0] == "not":
        cnfList[1] = cnfIff(cnfList[1])
    if cnfList[0] == "and":
        for i in range(1,len(cnfList)):
            cnfList[i] = cnfIff(cnfList[i])
    if cnfList[0] == "or":
        for i in range(1,len(cnfList)):
            cnfList[i] = cnfIff(cnfList[i])
    if cnfList[0] == "implies":
        cnfList[1] = cnfIff(cnfList[1])
        cnfList[2] = cnfIff(cnfList[2])
    if cnfList[0] == "iff":
        cnfList = cnfIff(["or",["implies",cnfList[1],cnfList[2]],["implies",cnfList[2],cnfList[1]]])
    return cnfList

def cnfImplies(cnfList):
    if isVariable(cnfList):
        return cnfList
    if cnfList[0] == "not":
        cnfList[1] = cnfImplies(cnfList[1])
    if cnfList[0] == "and":
        for i in range(1,len(cnfList)):
            cnfList[i] = cnfImplies(cnfList[i])
    if cnfList[0] == "or":
        for i in range(1,len(cnfList)):
            cnfList[i] = cnfImplies(cnfList[i])
    if cnfList[0] == "implies":
        cnfList = cnfImplies(["or",["not",cnfList[1]],cnfList[2]])
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

def cnfConvert(cnfList):
    if isVariable(cnfList):
        return cnfList
    if cnfList[0] == "not":
        if isinstance(cnfList[1],StringType) and len(cnfList[1]) == 1:
            return cnfList
        if isinstance(cnfList[1],ListType) and cnfList[1][0] == "not":
            return cnfConvert(cnfList[1][1])
        if isinstance(cnfList[1],ListType) and cnfList[1][0] == "and":
            notOrList = ["or"]
            for item in cnfList[1][1:]:
                notOrList.append(["not",item])
            return cnfConvert(notOrList)
        if isinstance(cnfList[1],ListType) and cnfList[1][0] == "or":
            notOrList = ["and"]
            for item in cnfList[1][1:]:
                notOrList.append(["not",item])
            return cnfConvert(notOrList)
    if cnfList[0] == "and":
        for i in range(1,len(cnfList)):
            cnfList[i] = cnfConvert(cnfList[i])
        cnfList = mergeAnd(cnfList)
        cnfList = deleteAndReturn(cnfList)
        return cnfList
    return cnfList

cnfList = ["not",["or","A","B"]]
print cnfConvert(cnfList)