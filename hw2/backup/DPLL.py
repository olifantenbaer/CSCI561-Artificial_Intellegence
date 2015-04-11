import sys
from types import*

#build symbol list
def buildSymbolList(cnfList):
    symbol = {}
    if cnfList[0] == "and":
        for i in range(1,len(cnfList)):
            if type(cnfList[i]) == StringType:
                item = cnfList[i]
                if not symbol.has_key(item):
                    symbol[item] = "true"
                continue
            if cnfList[i][0] == "not":
                item = cnfList[i][1]
                if not symbol.has_key(item):
                    symbol[item] = "true"
                continue
            for j in range(1,len(cnfList[i])):
                if type(cnfList[i][j]) == StringType:
                    item = cnfList[i][j]
                else:
                    item = cnfList[i][j][1]
                if not symbol.has_key(item):
                    symbol[item] = "true"
    elif cnfList[0] == "or":
        for i in range(1,len(cnfList)):
            if type(cnfList[i]) == StringType:
                item = cnfList[i]
            else:
                item = cnfList[i][1]
            if not symbol.has_key(item):
                symbol[item] = "true"
    else:
        if cnfList[0] == "not":
            item = cnfList[1]
        else:
            item = cnfList[0]
        if not symbol.has_key(item):
            symbol[item] = "true"
    return symbol

def find_pure_symbols(cnfList, symbolList):
    for key in symbolList.keys():
        flag1 = 0
        flag2 = 0
        item1 = str(key)
        item2 = ["not",str(key)]
        if cnfList[0] == "and":
            for i in range(1, len(cnfList)):
                if type(cnfList[i]) == StringType:
                    if cnfList[i] == item1:
                        flag1 = 1
                elif cnfList[i][0] == "not":
                    if cnfList[i] == item2:
                        flag2 = 1
                else:
                    if item1 in cnfList[i]:
                        flag1 = 1
                    if item2 in cnfList[i]:
                        flag2 = 1
            if flag1 == 1 and flag2 != 1:
                symbolList[key] = "true"
                return item1
            if flag1 != 1 and flag2 == 1:
                symbolList[key] = "false"
                return item2
        elif cnfList[0] == "or":
            if item1 in cnfList:
                flag1 = 1
            if item2 in cnfList:
                flag2 = 1
            if flag1 == 1 and flag2 != 1:
                symbolList[key] = "true"
                return item1
            if flag1 != 1 and flag2 == 1:
                symbolList[key] = "false"
                return item2
        else:
            if cnfList[0] == "not":
                if cnfList == item2:
                    flag2 = 1
            else:
                if cnfList[0] == item1:
                    flag1 = 1
            if flag1 == 1 and flag2 != 1:
                symbolList[key] = "true"
                return item1
            if flag1 != 1 and flag2 == 1:
                symbolList[key] = "false"
                return item2
    return "false"

def deletePureSymbol(cnfList,pureSymbol):
    if cnfList[0] == "and":
        i = 1
        len = len(cnfList)
        while i < len:
            if type(cnfList[i]) == StringType:
                if cnfList[i] == pureSymbol:
                    cnfList.remove(pureSymbol)
                    continue
            elif cnfList[i][0] == "not":
                if cnfList[i] == pureSymbol:
                    cnfList.remove(pureSymbol)
                    continue
            elif pureSymbol in cnfList[i]:
                cnfList.remove(cnfList[i])
                continue
            i = i + 1
    elif cnfList[0] == "or":
        if item1 in cnfList:
            flag1 = 1
        if item2 in cnfList:
            flag2 = 1
        if flag1 == 1 and flag2 != 1:
            symbolList[key] = "true"
            return item1
        if flag1 != 1 and flag2 == 1:
            symbolList[key] = "false"
            return item2
    else:
        if cnfList[0] == "not":
            if cnfList == item2:
                flag2 = 1
        else:
            if cnfList[0] == item1:
                flag1 = 1
        if flag1 == 1 and flag2 != 1:
            symbolList[key] = "true"
            return item1
        if flag1 != 1 and flag2 == 1:
            symbolList[key] = "false"
            return item2
    return "false"


def DPLL(cnfList, symbol):
    if not cnfList:
        return True
    for item in cnfList:
        if not item:
            return False
    p = find_pure_symbols(cnfList,symbol)
    if p != "false":
