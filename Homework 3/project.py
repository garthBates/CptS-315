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
    messages = fileRead.readlines()
    fileRead.close()

    return messages
    


################################################################ Main ################################################################

def main():
    messageList = populateMessageList(trainingCookieMessages)

    print(messageList)

if __name__ == "__main__":
    main()