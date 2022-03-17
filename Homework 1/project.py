##############################
# Garth Bates
# 11473063
# Homework 1
# Date Completed:
##############################

from itertools import combinations
from itertools import permutations

infile = "../Homework 1/browsing-data.txt"
#infile = "../Homework 1/browsingdata_50baskets.txt"
wordfile = "../Homework 1/words.txt"
outfile = "../Homework 1/output.txt"

#file_read = open(infile, 'r')
#lines = file_read.readlines()

support = 8
wordDict = {}       #{word: count}
pairDict = {}       #{(word1, word2): count}
tripleDict = {}     #{(word1, word2, word3): count}
topDict = {}        #{(tuple): confidence}

def uniqueWords(inputfile, wordfile):
    inwords = open(inputfile, 'r')
    contents = inwords.read()
    inwords.close()
    word_list = contents.split()

    output = open(wordfile, 'w')

    word_list = set(word_list)

    #return word_list
    for word in word_list:
        output.write(str(word) + '\n')

    return word_list

def populateWordDict(wordList, dict):
    for words in wordList:
        dict[words] = 0

def findX(inList, x):
    return inList.count(x)

def findWords(inputfile, inDict):
    fileRead = open(inputfile, 'r')
    lines = fileRead.readlines()
    fileRead.close()
    #print(lines)

    #words = lines.split()
    for line in lines:
        words = line.split()
        for word in words:
            #print(findX(words, word))
            total = inDict.get(word)
            total += 1
            inDict[word] = total
        #print(words)
    #    print(findX(words, i))

#replaces the current word list with words that meet the support threshold
def cleanWordList(wordList, wDict):  
    newWords = []
    for word in wordList:
        if wDict.get(word) >= support:
            newWords.append(word)

    return newWords

#populatues the pair dictionary with all possible pairs
def populatePairDict(wordList, pDict, wDict):
    combos = combinations(wordList, 2)
    for pairs in list(combos):
        pairDict[pairs] = 0

    return pairDict
#populates the triple dictionary with all pissible triples
def populateTripleDict(wordList, tDict, pDict):
    """
    triple = combinations(wordList, 3)
    for triples in list(triple):
        tDict[triples] = 0
    """
    wordSet = set()
    for pair in pDict:
        wordSet.add(pair[0])
        wordSet.add(pair[1])

    #print(list(wordSet))
    triples = combinations(list(wordSet), 3)
    for triple in triples:
        tDict[triple] = 0

    return tDict

def findTriples(inputfile, dict):
    fileRead = open(inputfile, 'r')
    lines = fileRead.readlines()
    fileRead.close()

    for line in lines:
        words = line.split()
        perms = permutations(words, 3)
        combosInDict(dict, perms)

def findPairs(inputfile, dict):
    fileRead = open(inputfile, 'r')
    lines = fileRead.readlines()
    fileRead.close()

    #print(lines)
    
    #for each line, creates all permutations of the words for that line.
    for line in lines:
        #print(line)
        words = line.split()
        perms = permutations(words, 2)
        #print(list(perms))
        combosInDict(dict, perms)


def combosInDict(dict, permList):
    for combos in permList:
        if combos in dict:
            total = dict.get(combos)
            total += 1
            dict[combos] = total

#removes all pairs that do not meet the support threshold
def cleanPairDict(pairDict):
    for pair in list(pairDict):
        if pairDict.get(pair) < support:
            del pairDict[pair]

def pairConfidence(pairDict, wordDict):
    pairs = pairDict.keys()
    words = wordDict.keys()
    confDict = {}
    for pair in pairs:
        confidence = pairDict.get(pair) / wordDict.get(pair[0])
        confDict[pair] = confidence

        confidence = pairDict.get(pair) / wordDict.get(pair[1])
        newTup = (pair[1], pair[0])
        confDict[newTup] = confidence
    return confDict

def tripleConfidence(tDict, wDict):
    triples = tDict.keys()
    words = wDict.keys()
    confDict = {}
    for triple in triples:
        confidence = tDict.get(triple) / wDict.get(triple[0])
        confDict[triple] = confidence

        confidence = tDict.get(triple) / wDict.get(triple[1])
        newTup = (triple[1], triple[0], triple[2])
        confDict[newTup] = confidence

        confidence = tDict.get(triple) / wDict.get(triple[2])
        newTup = (triple[2], triple[1], triple[0])
        confDict[newTup] = confidence

    return confDict


def topFive(confDict):
    pairs = confDict.keys()
    pairs = sorted(pairs)
    pairs.reverse()
    #print(pairs)
    top5 = [None, None, None, None, None]
    conf1 = -1
    conf2 = -1
    conf3 = -1
    conf4 = -1
    conf5 = -1

    for pair in pairs:
        #print(pair[0] + ' ' + pair[1] + ' ' + str(confDict.get(pair)))
        if confDict.get(pair) >= conf1:
            conf5 = conf4
            conf4 = conf3
            conf3 = conf2
            conf2 = conf1
            conf1 = confDict.get(pair)
            #print(conf1)
            top5[0] = pair[0] + ' ' + pair[1] + ' ' + str(confDict.get(pair))
            #print(top5[0])
            #print(top5[0][0:7])       
        elif confDict.get(pair) < conf1 and confDict.get(pair) >= conf2:
            conf5 = conf4
            conf4 = conf3
            conf3 = conf2
            conf2 = confDict.get(pair)
            top5[1] = str(pair[0] + ' ' + pair[1] + ' ' + str(confDict.get(pair)))
        elif confDict.get(pair) < conf2 and confDict.get(pair) >= conf3 :
            conf5 = conf4
            conf4 = conf3
            conf3 = confDict.get(pair)
            top5[2] = str(pair[0] + ' ' + pair[1] + ' ' + str(confDict.get(pair)))
        elif confDict.get(pair) < conf3 and confDict.get(pair) >= conf4:
            conf5 = conf4
            conf4 = confDict.get(pair)
            top5[3] = str(pair[0] + ' ' + pair[1] + ' ' + str(confDict.get(pair)))
        elif confDict.get(pair) < conf4 and confDict.get(pair) >= conf5:
            conf5 = confDict.get(pair)
            top5[4] = str(pair[0] + ' ' + pair[1] + ' ' + str(confDict.get(pair)))

    return top5
    
def reportResult(top5Pairs, top5Triples):
    print("OUTPUT A")
    for pair in top5Pairs:
        print(pair)

    print("\nOUTPUT B")
    for triple in top5Triples:
        print(triple)

def main():

    wordsList = list(uniqueWords(infile, wordfile))

    populateWordDict(wordsList, wordDict)
    #print(wordDict)
    findWords(infile, wordDict)
    #print(wordDict)
    wordsList = cleanWordList(wordsList, wordDict)
    #print(wordsList)

    populatePairDict(wordsList, pairDict, wordDict)
    #print("Before: ")
    #print(pairDict)
    findPairs(infile, pairDict)
    #print("Before: ")
    #print(pairDict)
    cleanPairDict(pairDict)
    #print(pairDict)

    #print(pairConfidence(pairDict, wordDict))

    #topFivePairs(pairConfidence(pairDict, wordDict))
    
    #print("OUTPUT A")
    #print(topFive(pairConfidence(pairDict, wordDict)))

    populateTripleDict(wordsList, tripleDict, pairDict)
    findTriples(infile, tripleDict)
    cleanPairDict(tripleDict)
    #print(tripleDict)
    #print(tripleConfidence(tripleDict, wordDict))
    #print("OUTPUT B")
    #print(topFive(tripleConfidence(tripleDict, wordDict)))

    reportResult(topFive(pairConfidence(pairDict, wordDict)), topFive(tripleConfidence(tripleDict, wordDict)))

    

if __name__ == "__main__":
    main()