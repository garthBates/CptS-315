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

def cleanMessage(message, stop):
    clean = message.replace(stop, '')
    return clean




################################################################ Main ################################################################

def main():
    messageList = populateMessageList(trainingCookieMessages)
    #print(messageList)

    print(cleanMessage("a new voyage will fill your life with untold memories", 'a'))


if __name__ == "__main__":
    main()