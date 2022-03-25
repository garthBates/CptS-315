##############################
# Garth Bates
# 11473063
# Homework 3
# Date Completed: 4/5/2022
##############################

stopWords = "../Homework 3/fortune-cookie-data/stoplist.txt"
trainingCookieMessages = "../Homework 3/fortune-cookie-data/traindata.txt"
trainingCookieLabels = "../Homework 3/fortune-cookie-data/trainlabels/txt"

trainingSetsDict = {}       #{phrase: label}
messageList = []            #A list of all the messages. Used to clean messages before populating the trainingSetDict
wordList = []               #A list of all unique words in the messages with the stop words removed.

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
    inWords = set(inWords)

    return inWords


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





################################################################ Main ################################################################

def main():
    messageList = populateMessageList(trainingCookieMessages)
    print(messageList)
    wordList = uniqueWords(trainingCookieMessages)
    print(wordList)


if __name__ == "__main__":
    main()