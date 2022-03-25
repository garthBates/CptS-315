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

############################################################ Pre-Processing ##########################################################
def populateMessageList(inputFile):
    fileRead = open(inputFile, 'r')
    messages = fileRead.read().splitlines()
    fileRead.close()

    return messages
    
def cleanMessageList(messages, inputFile):
    fileRead = open(inputFile, 'r')
    stops = fileRead.read().splitlines()
    fileRead.close()

    cleanList = []    
    for message in messages:
        for stop in stops:
            #cleanList.append(cleanMessage(message, stop))
            message = cleanMessage(message, stop)
            #print(message)
        cleanList.append(message)

    return cleanList

def cleanMessage(message, stop):
    #print(stop)
    subString = message.split(" ")
    if stop not in subString:
        return message
    else:
        #subString = message.split(" ")
        #subString.remove(str(stop))
        subString = list(filter((stop).__ne__, subString))
        clean = ' '.join(subString)
        return clean




################################################################ Main ################################################################

def main():
    messageList = populateMessageList(trainingCookieMessages)
    #print(messageList)

    #cleanMessage("a new voyage will fill your life with untold memories", 'a')
    messageList = cleanMessageList(messageList, stopWords)
    print(messageList)


if __name__ == "__main__":
    main()