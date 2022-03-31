##############################
# Garth Bates
# 11473063
# Homework 3
# Date Completed: 4/5/2022
##############################

import numpy as np

outFile = "../Homework 3/output.txt"

#Cookie Files
stopWords = "../Homework 3/fortune-cookie-data/stoplist.txt"
trainingCookieMessages = "../Homework 3/fortune-cookie-data/traindata.txt"
trainingCookieLabels = "../Homework 3/fortune-cookie-data/trainlabels.txt"
testingCookieMessages = "../Homework 3/fortune-cookie-data/testdata.txt"
testingCookieLabels = "../Homework 3/fortune-cookie-data/testlabels.txt"

#Vowel Files
trainingOCR = "../Homework 3/OCR-data/ocr_train.txt"
testingOCR = "../Homework 3/OCR-data/ocr_test.txt"

#Cookie data structures
trainingSetsList = []       #A list of tuples (vector, label) containing all message vectors and their label
testingSetsList = []        #A list of tuples (vector, label) containing all message vectors and their label
messageList = []            #A list of all the messages. Used to clean messages before populating the trainingSetDict
wordList = []               #A list of all unique words in the messages with the stop words removed.
trainingVectorList = []     #A list of all the vectors of size M, for each message
testingVectorList = []      #A list of all the vectors of size M, for each message
trainedVector = []          #A vector containing all the trained weights after learning algorithm
missList = []               #stores the count of misses for each iter. missList[0] will hold the total misses for iter 1 and so on
cookieWeightsLives = []     #A list of tuples (weight[i], c[i], iteration) where i is the index in the list
iterationWeights = []       #A list of the final weight after each iteration on the training alg.

#OCR data structures
ocrMessageList = []         #A list of all messages. Used to clean messages before populating ocrTrainingSetsList
trainingOCRSetsList = []    #A list of tuples (vector, label) containing all message vectors and their lebel
trainedOCRVector = []       #A vector containing all the trained weights after learning algorithm
testingOCRSetsList = []


learningRate = 1            #For Online Binary-Classifier Learning Alg. index 0 is iteration 1 index 19 is iteration 20

############################################################ Pre-Processing ##########################################################

##### Cookie Pre-Processing #####
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

##### OCR Pre-Processing #####
def cleanOCRMessages(tList):
    tempMessage = []
    for i in range(len(tList)):
        if tList[i] != "\n" and tList[i] != '\t' and tList[i] != "			":
            #tempMessage = tList[i][4:-4]
            tempMessage = tList[i].split("im")
            tempMessage = tempMessage[1][:-4]
            #print(tempMessage)
            tempMessage = tempMessage + (tList[i][-3])
            tList[i] = tempMessage

    clean = list(filter(("\t\t\t").__ne__, tList))
    return clean
  

def isVowel(inChar):
    c = inChar.lower()
    if c == 'a' or c == 'e' or c == 'i' or c == 'o' or c == 'u':
        return True
    else:
        return False

def buildOCRVector(message):
    vector = []
    if message != "\t\t\t":
        for i in range(len(message) - 1):
            #print(message[i])
            vector.append(int(message[i]))
    return vector

def buildOCRSetsList(mList, tList):
    for i in range(len(mList)):
        vector = buildOCRVector(mList[i])
        if isVowel(mList[i][-1]) == True:
            label = 1
        else:
            label = 0
        tList.append((vector, label))

def buildBlankOCRWordList(message):
    wordList = []
    for i in range(len(message)-1):
        wordList.append(0)

    return wordList

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
def buildSetList(tList, vList, infile):
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
            lives = 1
            xSubT = np.array(sets[0])
            yHat = xSubT.dot(w)                                         #       yHat = sign(w · xt) // predict using the current weights
            if yHat <= 0:                                               #       if mistake then
                #cookieWeightsLives.append((w,lives, i + 1))
                ySubT = np.array(sets[1])
                w = w + learningRate * (ySubT * xSubT)                  #           w = w + η · yt · xt // update the weights
                misses += 1
                lives = 1
            else:
                lives += 1
        missList.append(misses)
        iterationWeights.append(w)
    return w

def averagedPerceptron(tList, wList, tVector, iters):
    avgW = np.array(tVector)

    for i in range(iters):
        totalW = avgW
        for sets in tList:
            lives = 1
            xSubT = np.array(sets[0])
            yHat = xSubT.dot(totalW)
            if yHat <= 0:
                cookieWeightsLives.append((avgW, lives))
                ySubT = np.array(sets[1])
                avgW = avgW + learningRate * (ySubT * xSubT)
                totalW += avgW
                lives = 1
            else:
                lives += 1
    return avgW




def onlineBinaryClassifierTesting(tVector, iters, tList):
    accuracy = []
    w = np.array(tVector)
    for i in range(iters):
        hits = 0
        for sets in tList:
            xSubT = np.array(sets[0])
            yHat = xSubT.dot(w)
            if yHat > 0:
                hits += 1
        accuracy.append(hits / len(tVector))
    return accuracy


def reportResult(iters, cookieTestAccSTD, cookieTrainAccSTD, cookieTrainAccAVG, cookieTestAccAVG, ocrTrainAccSTD, ocrTestAccSTD, ocrTrainAccAVG, ocrTestAccAVG):
    output = open(outFile, 'w')

    #Cookie Block
    for i in range(iters):
        output.write(str(missList[i]) + "\n")

    for i in range(iters):
        output.write(str(cookieTrainAccSTD[i]) + " ")
        output.write(str(cookieTestAccSTD[i]) + "\n")

    output.write(str(cookieTrainAccAVG[-1]) + " ")
    output.write(str(cookieTestAccAVG[-1]) + " \n")


    #OCR Block
    for i in range(iters):
        output.write(str(missList[i+20]) + "\n")

    for i in range(iters):
        output.write(str(ocrTrainAccSTD[i]) + " ")
        output.write(str(ocrTestAccSTD[i]) + "\n")

    output.write(str(ocrTrainAccAVG[-1]) + " ")
    output.write(str(ocrTestAccAVG[-1]))


################################################################ Main ################################################################

def main():
    #Cooking Training
    print("Cookie Training")
    messageList = populateMessageList(trainingCookieMessages)
    wordList = uniqueWords(trainingCookieMessages)
    wordList = cleanWordList(wordList, stopWords)
    buildVectorList(wordList, trainingVectorList, messageList)
    buildSetList(trainingSetsList, trainingVectorList, trainingCookieLabels)
    finalCookieWeights = onlineBinaryClassifierLearning(trainingSetsList, wordList, trainedVector, 20)
    avgCookieWeights = averagedPerceptron(trainingSetsList, wordList, trainedVector, 20)
    cookieTestAccuracySTD = onlineBinaryClassifierTesting(finalCookieWeights, 20, trainingSetsList)
    cookieTestAccuracyAVG = onlineBinaryClassifierTesting(avgCookieWeights, 20, trainingSetsList)


    #Cookie Testing
    print("Cookie Testing")
    messageList = populateMessageList(testingCookieMessages)
    buildVectorList(wordList, testingVectorList, messageList)
    buildSetList(testingSetsList, testingVectorList, testingCookieLabels)
    cookieTrainingAccuracySTD = onlineBinaryClassifierTesting(finalCookieWeights, 20, testingSetsList)
    cookieTrainingAccuracyAVG = onlineBinaryClassifierTesting(avgCookieWeights, 20, testingSetsList)

    #Vowel Training
    print("Vowel Training")
    ocrMessageList = populateMessageList(trainingOCR)
    ocrMessageList = cleanOCRMessages(ocrMessageList)
    buildOCRSetsList(ocrMessageList, trainingOCRSetsList)
    ocrWordList = buildBlankOCRWordList(ocrMessageList[0])
    finalOCRweights = onlineBinaryClassifierLearning(trainingOCRSetsList, ocrWordList, trainedOCRVector, 20)
    avgORCWeights = averagedPerceptron(trainingOCRSetsList, ocrWordList, trainedOCRVector, 20)
    ocrTrainingAccuracySTD = onlineBinaryClassifierTesting(finalOCRweights, 20, trainingOCRSetsList)
    ocrTrainingAccuracyAVG = onlineBinaryClassifierTesting(avgORCWeights, 20, trainingOCRSetsList)

    #Vowel Testing
    print("Vowel Testing")
    ocrMessageList = populateMessageList(testingOCR)
    ocrMessageList = cleanOCRMessages(ocrMessageList)
    buildOCRSetsList(ocrMessageList, testingOCRSetsList)
    ocrTestAccuracySTD = onlineBinaryClassifierTesting(finalOCRweights, 20, testingOCRSetsList)
    ocrTestAccuracyAVG = onlineBinaryClassifierTesting(avgORCWeights, 20, testingOCRSetsList)
    
    #print(len(missList))
 

    reportResult(20, cookieTrainingAccuracySTD, cookieTestAccuracySTD, cookieTestAccuracyAVG, cookieTrainingAccuracyAVG, 
                ocrTrainingAccuracySTD, ocrTestAccuracySTD, ocrTrainingAccuracyAVG, ocrTestAccuracyAVG)


if __name__ == "__main__":
    main()