from types import *
import sys
def buildSymbolsOr(cnfList):
    symbols = {}
    for item in cnfList[1:]:
        if isinstance(item,StringType) and not symbols.has_key(item):
            symbols[item] = "true"
        if isinstance(item,ListType) and not symbols.has_key((item[1])):
            symbols[item[1]] = "false"
    return symbols

def buildSymbolsAnd(cnfList):
    symbols = {}
    for item in cnfList[1:]:
        if isinstance(item,ListType):
            #["not","A"]
            if item[0] == "not":
                #key exits
                if symbols.has_key(item[1]):
                    symbols[item[1]][1] = 1
                    symbols[item[1]][3] = 1
                else:
                    symbols[item[1]] = [0,1,0,1]
            else:
                #["or"..]
                for literal in item[1:]:
                    #["not"
                    if isinstance(literal,ListType):
                        #not key exits
                        if symbols.has_key(literal[1]):
                            symbols[literal[1]][1] = 1
                        else: #not key not exits
                            symbols[literal[1]] = [0,1,0,0]
                    else: #[""]
                        if symbols.has_key(literal):
                            symbols[literal][0] = 1
                        else:
                            symbols[literal] = [1,0,0,0]
        else:
            if symbols.has_key(item):
                symbols[item][0] = 1
                symbols[item][2] = 1
            else:
                symbols[item] = [1,0,1,0]
    return symbols

def isTrue(cnfList,model):
    for cluase in cnfList[1:]:
        if isinstance(cluase,StringType):
            if model.has_key(cluase) and model[cluase] == "true":
                continue
            else:
                return False
        if isinstance(cluase,ListType):
            if cluase[0] == "not":
                if model.has_key(cluase[1]) and model[cluase[1]] == "false":
                    continue
                else:
                    return False
            else:
                flag = 0
                for literal in cluase:
                    if isinstance(literal,StringType):
                        if model.has_key(literal) and model[literal] == "true":
                            flag = 1
                            break
                    else:
                        if model.has_key(literal[1]) and model[literal[1]] == "false":
                            flag = 1
                            break
                if  flag == 1:
                    continue
                else:
                    return False
    return True

def isFalse(cnfList,model):
    for cluase in cnfList[1:]:
        if isinstance(cluase,StringType):
            if (model.has_key(cluase) and model[cluase] == "false") or cluase == "false":
                return True
            else:
                continue
        if isinstance(cluase,ListType):
            if cluase[0] == "not":
                if model.has_key(cluase[1]) and model[cluase[1]] == "true":
                    return True
                else:
                    continue
            else:
                flag = 0
                for literal in cluase:
                    if isinstance(literal,StringType):
                        if model.has_key(literal) and model[literal] == "false":
                            flag = flag + 1
                    else:
                        if model.has_key(literal[1]) and model[literal[1]] == "true":
                            flag = flag + 1
                if  flag == len(cluase) - 1:
                    return True
                else:
                    continue
    return False

def findPureSymbols(symbols):
    for k,v in symbols.items():
        if v[0] == 1 and v[1] == 0:
            return k,"true"
        elif v[0] == 0 and v[1] == 1:
            return k,"false"
    return None,None

def findUnitClause(symbols):
    for k,v in symbols.items():
        if v[2] == 1:
            return k,"true"
        elif v[3] == 1:
            return k,"false"
    return None,None

def removeClausesPure(cnfList,symbol,model):
    length = len(cnfList)
    i = 1
    if model[symbol] == "true":
        removeItem = symbol
        while i < length:
            if isinstance(cnfList[i],ListType) and cnfList[i][0] == "or":
                if removeItem in cnfList[i]:
                    cnfList.remove(cnfList[i])
                    length = length - 1
                    continue
                i = i + 1
            elif isinstance(cnfList[i],StringType):
                if removeItem == cnfList[i]:
                    cnfList.remove(cnfList[i])
                    length = length - 1
                    continue
                i = i + 1
            else:
                i = i + 1
    else:
        removeItem = ["not",symbol]
        while i < length:
            if isinstance(cnfList[i],ListType) and cnfList[i][0] == "or":
                if removeItem in cnfList[i]:
                    cnfList.remove(cnfList[i])
                    length = length - 1
                    continue
                i = i + 1
            elif isinstance(cnfList[i],ListType) and cnfList[i][0] == "not":
                if removeItem == cnfList[i]:
                    cnfList.remove(cnfList[i])
                    length = length - 1
                    continue
                i = i + 1
            else:
                i = i + 1
    return cnfList

def removeClusesUnit(cnfList,symbol,model):
    removeItem1 = symbol
    removeItem2 = ["not",symbol]
    if model[symbol] == "true":
        cnfList = removeClausesPure(cnfList,symbol,model)
        i = 1
        length = len(cnfList)
        while i < length:
            if isinstance(cnfList[i],ListType) and cnfList[i][0]== "not":
                if cnfList[i] == removeItem2:
                    cnfList[i] = "false"
                i = i + 1
            elif isinstance(cnfList[i],ListType) and cnfList[i][0] == "or":
                if removeItem2 in cnfList[i]:
                    cnfList[i].remove(removeItem2)
                    if len(cnfList[i]) == 1:
                        cnfList[i] = "false"
                i = i + 1
            else:
                i = i + 1
    else:
        cnfList = removeClausesPure(cnfList,symbol,model)
        i = 1
        length = len(cnfList)
        while i < length:
            if isinstance(cnfList[i],StringType):
                if cnfList[i] == removeItem1:
                    cnfList[i] = "false"
                i = i + 1
            elif isinstance(cnfList[i],ListType) and cnfList[i][0] == "or":
                if removeItem1 in cnfList[i]:
                    cnfList[i].remove(removeItem1)
                    if len(cnfList[i]) == 1:
                        cnfList[i] = "false"
                i = i + 1
            else:
                i = i + 1
    return cnfList

def DPLL(cnfList,model):
    symbols = buildSymbolsAnd(cnfList)
    if isTrue(cnfList,model):
        return True,model
    if isFalse(cnfList,model):
        return False,model
    symbol,v = findPureSymbols(symbols)
    if symbol != None:
        model[symbol] = v
        cnfList = removeClausesPure(cnfList,symbol,model)
        return DPLL(cnfList,model)
    symbol,v = findUnitClause(symbols)
    if symbol != None:
        model[symbol] = v
        cnfList = removeClusesUnit(cnfList,symbol,model)
        return DPLL(cnfList,model)
    symbol = symbols.keys()[0]
    #symbol = true
    modelTrue = model
    cnfListTrue = cnfList
    modelTrue[symbol] = "true"
    cnfListTrue = removeClusesUnit(cnfListTrue,symbol,modelTrue)
    #symbol = false
    modelFalse = model
    cnfListFalse = cnfList
    modelFalse[symbol] = "false"
    cnfListFalse = removeClusesUnit(cnfListFalse,symbol,modelTrue)
    return DPLL(cnfListTrue,modelTrue) or DPLL(cnfListFalse,modelFalse)


def main():
#    inputFile = open(sys.argv[2],"r")
    inputFile = open("CNF_sentences.txt","r")
    outputFile = open("CNF_satisfiability.txt","w")
    sentenceNum = int(inputFile.readline())
    for i in range(0,sentenceNum):
        cnfList = eval(inputFile.readline())
        model = {}
        output = []
        #one "or" clause
        if cnfList[0] == "or":
            symbols = buildSymbolsOr(cnfList)
            output.append("true")
            for k,v in symbols.items():
               output.append(k+"="+v)
        if cnfList[0] == "not":
            output.append("true")
            output.append(cnfList[1]+"=false")
        if len(cnfList) == 1:
            output.append("true")
            output.append(cnfList[0]+"=true")
        if cnfList[0] == "and":
            symbols = buildSymbolsAnd(cnfList)
            saveSymbols = symbols
            model = {}
            result,model = DPLL(cnfList,model)
            if result == False:
                output.append("false")
            else:
                output.append("true")
                for item in symbols.keys():
                    if model.has_key(item):
                        output.append(item+"="+model[item])
                    else:
                        output.append(item+"=true")
        outputFile.write(repr(output)+"\n")




main()
