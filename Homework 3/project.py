##############################
# Garth Bates
# 11473063
# Homework 3
# Date Completed: 4/5/2022
##############################

import numpy as np

stopWords = "../Homework 3/fortune-cookie-data/stoplist.txt"
trainingCookieMessages = "../Homework 3/fortune-cookie-data/traindata.txt"
trainingCookieLabels = "../Homework 3/fortune-cookie-data/trainlabels.txt"

trainingSetsList = []       #A list of tuples (vector, label) containing all message vectors and their label
messageList = []            #A list of all the messages. Used to clean messages before populating the trainingSetDict
wordList = []               #A list of all unique words in the messages with the stop words removed.
vectorList = []             #A list of all the vectors of size M, for each message
trainedVector = []          #A vector containing all the trained weights after learning algorithm
missList = []               #stores the count of misses for each iter. missList[0] will hold the total misses for iter 1 and so on

learningRate = 1            #For Online Binary-Classifier Learning Alg.

############################################################ Pre-Processing ##########################################################
def populateMessageList(inputFile):
    fileRead = open(inputFile, 'r')
    messages = fileRead.read().splitlines()
    fileRead.close()

    return messages
    
def uniqueWords(inputFile):
    fileRead = open(inputFile, 'r')
    contents = fileRead.read()
    fileRead.close()

    inWords = contents.split()
    inWords = list(set(inWords))

    return inWords

def cleanWordList(wList, inputFile):
    fileRead = open(inputFile, 'r')
    stops = fileRead.read().splitlines()
    fileRead.close()

    for stop in stops:
        if stop in wList:
            wList.remove(stop)

    wList.sort()
    return wList

def buildVector(wList, message):
    vector = []
    for word in wList:
        if word not in message:
            vector.append(0)
        else:
            vector.append(1)
    return vector

def buildVectorList(wList, vList, mList):
    for message in mList:
        vList.append(buildVector(wList, message))


### Begin Usless Functions
def cleanMessageList(messages, inputFile):
    fileRead = open(inputFile, 'r')
    stops = fileRead.read().splitlines()
    fileRead.close()

    cleanList = []    
    for message in messages:
        for stop in stops:
            message = cleanMessage(message, stop)
        cleanList.append(message)

    return cleanList

def cleanMessage(message, stop):
    subString = message.split(" ")
    if stop not in subString:
        return message
    else:
        subString = list(filter((stop).__ne__, subString))
        clean = ' '.join(subString)
        return clean
### End Usless Functions

############################################################ Classification ##########################################################
def buildTrainingetList(tList, vList, infile):
    fileRead = open(infile, 'r')
    labels = fileRead.read().splitlines()
    fileRead.close()

    for i in range(len(vList)):
        tList.append((vList[i], int(labels[i])))

def onlineBinaryClassifierLearning(tList, wList, tVector, iters):
    #Initialze the weights w=0
    for word in wList:
        tVector.append(0)

    

    w = np.array(tVector)
    for i in range(iters):                                              #for each training iteration itr ∈ {1, 2, · · · , T } do
        misses = 0
        for sets in tList:                                              #   for each training example (xt, yt) ∈ D do
            #print(sets[0])
            xSubT = np.array(sets[0])
            yHat = xSubT.dot(w)                                         #       yHat = sign(w · xt) // predict using the current weights
            if yHat <= 0:                                               #       if mistake then
                ySubT = np.array(sets[1])
                w = w + learningRate * (ySubT * xSubT)                  #           w = w + η · yt · xt // update the weights
                misses += 1
                #w = (ySubT * xSubT)
                #print(w)
        missList.append(misses)
    return w


def onlineBinaryClassifierTesting(tVector, iters, tList):
    accuracy = []
    w = np.array(tVector)
    for i in range(iters):
        hits = 0
        for sets in tList:
            xSubT = np.array(sets[0])
            yHat = xSubT.dot(w)
            




################################################################ Main ################################################################

def main():
    messageList = populateMessageList(trainingCookieMessages)
    wordList = uniqueWords(trainingCookieMessages)
    wordList = cleanWordList(wordList, stopWords)

    buildVectorList(wordList, vectorList, messageList)

    buildTrainingetList(trainingSetsList, vectorList, trainingCookieLabels)
    #print(trainingSetsList)

    finalWeights = onlineBinaryClassifierLearning(trainingSetsList, wordList, trainedVector, 20)
    print(finalWeights)
    print(missList)



if __name__ == "__main__":
    main()