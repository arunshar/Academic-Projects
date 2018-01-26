from numpy import *
import operator
import timeit
import sys
import itertools 
from collections import defaultdict
from optparse import OptionParser

def loadDataSet(fileName, delim='\t'):
    fr = open(fileName)
    stringArr = [line.strip().split(delim) for line in fr.readlines()]
    for x in range(0, len(stringArr)):
        for y in range(0, len(stringArr[x])):
            if(y!=100):
                stringArr[x][y] = 'G' + str(y+1) + '_' + stringArr[x][y]                
    
    return array(stringArr)

def loadRuleFile(ruleFileName, delim='\n'):
    fr = open(ruleFileName)
    stringArr = [line.replace('\n','') for line in fr.readlines()]
    return stringArr

def createDataSet(dataSet):
    elements = []
    transactionList = []
    for rowData in dataSet:
        transactionList.append(rowData)
        for colValue in rowData:
            if not [colValue] in elements:
                elements.append([colValue])
    return list(map(frozenset, elements)) , list(map(set, transactionList))

def joinSet(itemSet, length):
    return set(map(lambda m : m[0].union(m[1]),set(filter(lambda m : len(m[0].union(m[1])) == length, itertools.combinations(itemSet, 2)))))

def findMinimumSupportItemList(uniqueItemset, transactionList, minSupport,freqSetDict):
    
    listSize = len(transactionList)
    
    localSetDict = defaultdict(int)
    
    for item in uniqueItemset:
        for transaction in transactionList:
            if item.issubset(transaction):
                freqSetDict[item] += 1
                localSetDict[item] += 1

    itemSet = set(map(lambda x:x[0],list(filter(lambda args : args[1]/listSize >= minSupport, localSetDict.items()))))
    
    return itemSet

def findFrequentItemSets(fileName, minSupport = 0.5):
    globalFreqList = dict()
    
    freqSetDict = defaultdict(int)
    
    data = loadDataSet(fileName)
        
    uniqueItemset,transactionList = createDataSet(data)
    
    transactionCount = len(transactionList)
    
    singleElementFreqList = findMinimumSupportItemList(uniqueItemset,transactionList,minSupport,freqSetDict)
    
    currentLSet = singleElementFreqList
    
    k = 2
        
    while(currentLSet != set([])):
        globalFreqList[k-1] = currentLSet
        currentLSet = joinSet(currentLSet, k)
        currentCSet = findMinimumSupportItemList(currentLSet,transactionList,minSupport,freqSetDict)
        currentLSet = currentCSet
        k = k + 1        
    
    return globalFreqList,freqSetDict,transactionCount

def generateSubsets(arr):
    subsetList = []
    for L in range(1, len(arr)+1):
        for subset in itertools.combinations(arr, L):
            subsetList.append(subset)
    return map(frozenset, subsetList)

def generateRules(globalFreqList, freqSetDict, transactionCount, minConfidence = 0.7):
    rulesList = []
    rulesDict = dict()
    for key, value in globalFreqList.items():
        if(key > 1):
            for item in value:
                subsets = generateSubsets(item)
                for element in subsets:
                    if len(item.difference(element)) > 0:
                        confidence = freqSetDict[item]/freqSetDict[element]
                        if confidence >= minConfidence:
                            rulesDict[((frozenset(element),frozenset(item.difference(element))))] = confidence
    return rulesDict

def apriori(fileName, minSupport = 50, minConfidence = 70):
    
    start_time = timeit.default_timer()
    
    globalFreqList,freqSetDict,transactionCount = findFrequentItemSets(fileName,minSupport/100)
    
    rulesDict = generateRules(globalFreqList,freqSetDict,transactionCount,minConfidence/100)
          
    elapsed = timeit.default_timer() - start_time
    print(elapsed)
    
    return globalFreqList,rulesDict

def printPart1Answers(globalFreqList):
    k = len(globalFreqList)
    count = 0;
    for i in range(0,k):
        count += len(globalFreqList[i+1])
        print("Number of length-"+str(i+1)+ " frequent itemsets : " + str(len(globalFreqList[i+1])))
    print("Number of all length frequent itemsets : " + str(count))

def printRules(rulesDict):
    for key, value in rulesDict.items():
        print(str(tuple(key[0])) +" --> " +str(tuple(key[1])) +" : "+str(value))

def substractDictionary(dictA,dictB):
    return {k: v for k, v in dictA.items() if k not in dictB}

def mergeDictionary(dictA,dictB):
    dictC = dictA.copy()
    dictC.update(dictB)
    return dictC

def dictionaryIntersection(dictA,dictB):
    return {x:dictA[x] for x in dictA if x in dictB}

def parseTemplate1Query(query):
    data = query.split("[")
    
    identifier, association = data[0][:-1].split(",")
        
    y = data[1].replace("]","")
    z = y.split(",")
    
    res = []
    
    for element in z:
        t = ()
        t += (element[1:-1],)
        res.append(frozenset(t))
    return identifier, association, res

def parseTemplate2Query(query):
    
    data = query.split(",")
    identifier = data[0]
    size = int(data[1])
    
    return identifier,size

def parseTemplate3Query(query):
    
    data = query.split(",")
    queryType1 = data[0][0:1]
    queryType2 = data[0][-1:]
    
    queryOperator = data[0][1:-1]
    query1 = ''
    query2 = ''
    
    if(queryType1 == '1' and queryType2 == '1'):
        query1 = data[1]+","+data[2]+","+data[3]
        query2 = data[4]+","+data[5]+","+data[6]
    elif(queryType1 == '1' and queryType2 == '2'):
        query1 = data[1]+","+data[2]+","+data[3]
        query2 = data[4]+","+data[5]
        
    if(queryType1 == '2' and queryType2 == '1'):
        query1 = data[1]+","+data[2]
        query2 = data[3]+","+data[4]+","+data[5]
    elif(queryType1 == '2' and queryType2 == '2'):
        query1 = data[1]+","+data[2]
        query2 = data[3]+","+data[4]   
    
    return queryOperator,queryType1,queryType2,query1,query2    

def template1(query,rulesDict):
    identifier, association, res = parseTemplate1Query(query)
    
    result = dict()
    
    if association == 'ANY':
        result = searchAny(rulesDict,identifier,res)
    elif association == 'NONE':
        result = searchNone(rulesDict,identifier,res)
    elif association == '1':
        result = searchSingle(rulesDict,identifier,res)
    return result

def template2(query,rulesDict):
    identifier, size = parseTemplate2Query(query)
    result = dict()
    for key,value in rulesDict.items():
        body = key[0]
        head = key[1]
        if(identifier == 'BODY' and len(body) >= size):
            result[key] = value
        elif(identifier == 'HEAD' and len(head) >= size):
            result[key] = value
        elif(identifier == 'RULE' and (len(body)+len(head) >= size)):
            result[key] = value
    return result

def template3(query,rulesDict):
    queryOperator,queryType1,queryType2,query1,query2 = parseTemplate3Query(query)
    
    result1 = dict()
    result2 = dict()
    
    result = dict()
    
    if(queryType1 == '1'):
        result1 = template1(query1,rulesDict)
    else:
        result1 = template2(query1,rulesDict)
        
    if(queryType2 == '1'):
        result2 = template1(query2,rulesDict)
    else:
        result2 = template2(query2,rulesDict)
        
    if(queryOperator == 'or'):
        result = mergeDictionary(result1,result2)
    else:
        result = dictionaryIntersection(result1,result2)
    return result
    

def searchAny(rulesDict,identifier,res):
    result = dict()
    for key,value in rulesDict.items():
        body = key[0]
        head = key[1]
        for item in res:
            if(identifier == 'BODY' and item.issubset(body)):
                result[key] = value
            elif(identifier == 'HEAD' and item.issubset(head)):
                result[key] = value
            elif(identifier == 'RULE' and (item.issubset(body) or item.issubset(head))):
                result[key] = value
    return result

def searchNone(rulesDict,identifier,res):
    
    result = searchAny(rulesDict,identifier,res)
    
    return substractDictionary(rulesDict,result)

def searchSingle(rulesDict,identifier,res):
    result = dict()
    
    for key,value in rulesDict.items():
        body = key[0]
        head = key[1]
        check = False
        for item in res:
            if(identifier == 'BODY' and item.issubset(body)):
                if check == False:
                    check = True
                else:
                    check = False
                    break
            elif(identifier == 'HEAD' and item.issubset(head)):
                if check == False:
                    check = True
                else:
                    check = False
                    break
            elif(identifier == 'RULE' and (item.issubset(body) or item.issubset(head))):
                if check == False:
                    check = True
                else:
                    check = False
                    break
        if(check == True):
            result[key] = value
    return result

if __name__ == "__main__":

    optparser = OptionParser()
    optparser.add_option('-f', '--inputFile',
                         dest='input',
                         help='filename containing data',
                         default=None)
    optparser.add_option('-s', '--minSupport',
                         dest='minS',
                         help='minimum support value',
                         default=50,
                         type='float')
    optparser.add_option('-c', '--minConfidence',
                         dest='minC',
                         help='minimum confidence value',
                         default=60,
                         type='float')
    optparser.add_option('-r', '--ruleFile',
                         dest='rules',
                         help='filename containing rules',
                         default=None)

    (options, args) = optparser.parse_args()

    fileName = None
    if options.input is None:
        fileName = sys.stdin
    elif options.input is not None:
        fileName = options.input
    else:
        print ('Data File Missing\n')
        sys.exit('System will exit')
        
    ruleFileName = None
    if options.input is None:
        ruleFileName = sys.stdin
    elif options.input is not None:
        ruleFileName = options.rules
    else:
        print ('Rule File Missing\n')
        sys.exit('System will exit')

    minSupport = options.minS
    minConfidence = options.minC

    freqItemSet, rulesDict = apriori(fileName,minSupport,minConfidence)
    printPart1Answers(freqItemSet)
    
    rulesList=loadRuleFile(ruleFileName)
    
    for rule in rulesList:
        query = rule[3:]
        if(rule.startswith('T1')):
            result = template1(query,rulesDict)
            print(query + " : " + str(len(result)))
            printRules(result)
        elif(rule.startswith('T2')):
            result = template2(query,rulesDict)
            print(query + " : " + str(len(result)))
            printRules(result)
        else:
            result = template3(query,rulesDict)
            print(query + " : " + str(len(result)))
            printRules(result)
        print('\n')
    



































