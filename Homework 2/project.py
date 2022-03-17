##############################
# Garth Bates
# 11473063
# Homework 2
# Date Completed: 3/11/2022
##############################

from itertools import combinations
from itertools import permutations
import math
from tkinter import N
import os

movieFile = "../Homework 2/movies.csv"
ratingFile = "../Homework 2/ratings.csv"
#movieFile = "../Homework 2/testmovies.csv"
#ratingFile = "../Homework 2/testratings.csv"
outFile = "../Homework 2/output.txt"


debuggingFile = "../Homework 2/similarity-matrix-debugging-information.csv"

movieDict = {}      #{movieID: (userID, rating)}
estimateDict = {}   #{userID: (movieID, estimate rating)}
neighborDict = {}   #{movieID: [n1, n2, n3, n4, n5]}
similarityDict = {} #{(movieID1, movieID2): similarity}
activeRatings = {}  #{user: [movie1, movie2, ... , movieN]} holds a list of all movies user has rated
totalUserCount = 0
neighbors = 2

################################ Part A: Construct a profile on each item (movie) ################################

def populateMovieDict(inputfile, dict):
    fileRead = open(inputfile, 'r')
    lines = fileRead.readlines()
    fileRead.close()

    lines.pop(0)
    for line in lines:
        lineList = line.split(',')
        dict[lineList[0]] = []

    return dict

def populateRatings(inputfile, dict):
    fileRead = open(inputfile, 'r')
    lines = fileRead.readlines()
    fileRead.close()
    lines.pop(0)
    for line in lines:
        lineList = line.split(',')
        newTup = (lineList[0], lineList[2])         #(userID, rating)
        rates = dict[lineList[1]]
        rates.append(newTup)
        dict[lineList[1]] = rates


    return dict

################################ Part B: Compute similarity score for movie-movie pairs via centered cosine ################################
def totalUsers(inputfile, count):
    fileRead = open(inputfile, 'r')
    lines = fileRead.readlines()
    fileRead.close()

    currentUser = 0

    lines.pop(0)
    for line in lines:
        lineList = line.split(',')
        if currentUser != lineList[0]:
            count = count + 1
            currentUser = lineList[0]

    return count

def centerItemScore(count, key, dict):
    totalScore = 0
    scores = dict[key]

    for score in scores:
        totalScore += float(score[1])

    average = totalScore/count
    
    newScores = []
    for score in scores:

        #print(score)
        centeredScore = float(score[1]) - average
        scoreList = list(score)
        scoreList[1] = centeredScore
        
        newScores.append(tuple(scoreList))
    #print(newScores)
    dict[key] = newScores



def centerAllScores(count, dict):
    for key in dict.keys():
        #print(key)
        centerItemScore(count, key, dict)
    
    return dict

def dotProducts(count, dict, key1, key2):
    product = 0

    movie1 = dict[key1]
    movie2 = dict[key2]

    list1 = []
    list2 = []

    for i in range((count)):
        '''
        if 0 <= i < len(movie1):
            if int(movie1[i][0]) > i + 1:
                #print("insert dot prod")
                movie1.insert(i, (str(i + 1), 0.0))
        if len(movie1) < count:
            movie1.append((str(i + 1), (0.0)))
        '''

        list1.append(movie1[i][1])

    for j in range((count)):
        '''
        if 0 <= j < len(movie2):
            if int(movie2[j][0]) > j + 1:
                #print("insert dot prod 2")
                movie2.insert(j, (str(j + 1), 0.0))
                #list2.append(movie2[j][1])
        if len(movie2) < count: 
            movie2.append((str(j + 1), (0.0)))
        '''
        #print(list2)
        list2.append(movie2[j][1])

    #print(movie1)
    #print(movie2)

    #print(list1)
    #print(list2)

    for k in range(count):
        product += list1[k] * list2[k]

    return(product)


def magnitude(count, dict, key):
    mag = 0

    movie = dict[key]
    rates = []

    for i in range(count):
        '''
        if 0 <= i < len(movie):
            if int(movie[i][0]) > i + 1:
                #print("insert mag")
                movie.insert(i, (str(i + 1), 0.0))
            #print(movie[i])
        if len(movie) < count:
            movie.append((str(i + 1), (0.0)))
        '''
        rates.append(movie[i][1])

    for j in range(count):
        mag += rates[j] * rates[j]

    mag = math.sqrt(mag)
    #print(mag)
    return mag

def computeCosineSimilarity(count, dict, key1, key2):
    dotProd = dotProducts(count, dict, key1, key2)
    mag1 = magnitude(count, dict, key1)
    mag2 = magnitude(count, dict, key2)
    if mag1 != 0 and mag2 != 0:
        similarity = dotProd / (mag1 * mag2)
        return(similarity)
    else:
        return 0

def populateSimilarityDict(count, movies, similarities):
    movieIDs = movies.keys()
    combos = combinations(movieIDs, 2)
    for movie in movieIDs:
        addBlanks(count, movies, movie)
    
    for pair in list(combos):
        similarities[pair] = computeCosineSimilarity(count, movies, pair[0], pair[1])
    return similarities

def addBlanks(count, dict, key):
    if key in dict:
        movies = dict[key]
        for i in range(count):
            if 0 <= i < len(movies):
                if int(movies[i][0]) > i + 1:
                    movies.insert(i, (str(i + 1), 0.0))

        if len(movies) < count:
            diff = count - len(movies)
            for i in range(diff):
                movies.append((str(i + diff), (0.0)))
    
        dict[key] = movies    


######################################## Part C: Compute the neighborhood set N for each item ########################################
def findNeighbors(similarityDict, key1):
    pairs = similarityDict.keys()
    pairs = sorted(pairs)

    hood = [None, None, None, None, None]

    sim1 = -1
    sim2 = -1
    sim3 = -1
    sim4 = -1
    sim5 = -1

    for sims in similarityDict.keys():
        if sims[0] == key1 or sims[1] == key1:
            if similarityDict[sims] >= sim1:
                sim5 = sim4
                sim4 = sim3
                sim3 = sim2
                sim2 = sim1
                sim1 = similarityDict[sims]
                hood[4] = hood[3]
                hood[3] = hood[2]
                hood[2] = hood[1]
                hood[1] = hood[0]
                hood[0] = sims
                #sim1 = sims
            elif similarityDict[sims] < sim1 and similarityDict[sims] >= sim2:
                sim5 = sim4
                sim4 = sim3
                sim3 = sim2
                sim2 = similarityDict[sims]
                hood[4] = hood[3]
                hood[3] = hood[2]
                hood[2] = hood[1]
                hood[1] = sims
            elif similarityDict[sims] < sim2 and similarityDict[sims] >= sim3:
                sim5 = sim4
                sim4 = sim3
                sim3 = similarityDict[sims]
                hood[4] = hood[3]
                hood[3] = hood[2]
                hood[2] = sims
            elif similarityDict[sims] < sim3 and similarityDict[sims] >= sim4:
                sim5 = sim4
                sim4 = similarityDict[sims]
                hood[4] = hood[3]
                hood[3] = sims
            elif similarityDict[sims] < sim4 and similarityDict[sims] >= sim5:
                sim5 = similarityDict[sims]
                hood[4] = sims

    return hood

def populateNeighborhood(neighborDict, similarityDict, movieDict):

    for movie in movieDict.keys():
        neighborDict[movie] = findNeighbors(similarityDict, movie)

    return neighborDict

##################################### Part D: Estimate rating of users who didn't rate this item #####################################
def buildEsitDict(count, estiDict):
    for i in range(count):
        estiDict[i+1] = []

def populateActiveRatings(inputfile, dict):
    fileRead = open(inputfile, 'r')
    lines = fileRead.readlines()
    fileRead.close()

    lines.pop(0)
    for line in lines:
        lineList = line.split(',')
        if lineList[0] in dict:
            newList = dict[lineList[0]]
            newList.append(lineList[1])
            dict[lineList[0]] = newList
        else:
            dict[lineList[0]] = [lineList[1]]
    return dict

def hasRated(activeDict, movieID, userID):
    actives = activeDict[userID]
    #print(actives)
    #print(userID)
    
    if movieID in actives:
        #print(str(userID) + " has rated movie " + str(movieID))
        return True
    else:
        #print(str(userID) + " has NOT rated movie " + str(movieID))
        return False
    

def estimateRating(simsDict, neighborsDict, ratingsDict, activeDict, movieID, userID):
    #print("movie ID: " + movieID, " userID: " + userID)
    hood = neighborsDict[movieID]   #neighbors of current movie
    cleanHood = []                  #pull neighbor IDs out of tuples
    hoodSims = {}                   #sims of all neighbors with current movie   {simID: simScore}
    userRatings = {}                #ratings of all neighbors by user {movieID: rating}

    for neighbor in hood:
        if neighbor[0] != movieID:
            cleanHood.append(neighbor[0])
        else:
            cleanHood.append(neighbor[1])

    
    ratedHood = []
    estimateMovie = False                   #the movie getting the estimate

    if hasRated(activeDict, movieID, userID) is True:   #if the movie has already been rated, dont estimate
        return None
    for movie in cleanHood:
        #print(movie)
        if hasRated(activeDict, movie, userID) is True:
            ratedHood.append(movie)

    #print(ratedHood)

    for neighbor in cleanHood:
        if (movieID, neighbor) in simsDict:
            #hoodSims.append(simsDict[(movieID, neighbor)])
            hoodSims[neighbor] = simsDict[(movieID, neighbor)]
        else:
            #hoodSims.append(simsDict[(neighbor, movieID)])
            hoodSims[neighbor] = simsDict[(neighbor, movieID)]

    for neighbor in cleanHood:
        #print(ratingsDict[neighbor])
        temp = ratingsDict[neighbor]
        for i in range(len(temp)):
            if temp[i][0] == userID:
                #userRatings.append((neighbor, temp[i][1]))      #[(movieID, rating)]
                userRatings[neighbor] = temp[i][1]

    #print(ratedHood)

    numerator = 0.0
    denominator = 0.0
    for i in range(len(ratedHood)):
        numerator += float(userRatings[ratedHood[i]]) * float(hoodSims[ratedHood[i]])
        denominator += float(hoodSims[ratedHood[i]])

    estimate = numerator/denominator
    
    #print("Clean hood: ")
    #print(cleanHood)
    #print("Hood sims: ")
    #print(hoodSims)
    #print("User Ratings: ")
    #print(userRatings)
    #print("Numerator: " + str(numerator))
    #print("Denominator: "+ str(denominator))
    #print("Estimate Rating: " + str(estimate))
    

    #print(cleanHood)
    #print(hoodSims)

    return estimate

def populateEstimates(count, simsDict, neighborsDict, ratingsDict, activeDict, estiDict):

    for i in range(count):
        for movie in ratingsDict.keys():
            estimate = (str(movie), estimateRating(simsDict, neighborsDict, ratingsDict, activeDict, str(movie), str(i + 1)))
            if estimate[1] != None:
                #estiDict[movie] = estimate
                #print("User ID: " + str(i + 1))
                #print("Estimate Rating: " + str(estimate))
                tempList = estiDict[i+1]
                tempList.append(estimate)
                estiDict[i+1] = tempList

    return estiDict

########################################## Part E: Compute recommended movies for each user ##########################################
def top5Recomemndations(estiDict, user):
    recs = estiDict[user]
    #print(recs)

    top5 = [None, None, None, None, None]

    rec1 = 0
    rec2 = 0
    rec3 = 0
    rec4 = 0
    rec5 = 0
    
    for i in range(len(recs)):
        #print(recs[i][1])
        if recs[i][1] > rec1:
            rec5 = rec4
            rec4 = rec3
            rec3 = rec2
            rec2 = rec1
            rec1 = recs[i][1]
            top5[4] = top5[3]
            top5[3] = top5[2]
            top5[2] = top5[1]
            top5[1] = top5[0]
            top5[0] = recs[i][0]
        elif recs[i][1] < rec1 and recs[i][1] >= rec2:
            rec5 = rec4
            rec4 = rec3
            rec3 = rec2
            rec2 = recs[i][1]
            top5[4] = top5[3]
            top5[3] = top5[2]
            top5[2] = top5[1]
            top5[1] = recs[i][0]
        elif recs[i][1] < rec2 and recs[i][1] >= rec3:
            rec5 = rec4
            rec4 = rec3
            rec3 = recs[i][1]
            top5[4] = top5[3]
            top5[3] = top5[2]
            top5[2] = recs[i][0]
        elif recs[i][1] < rec3 and recs[i][1] >= rec4:    
            rec5 = rec4
            rec4 = recs[i][1]
            top5[4] = top5[3]
            top5[3] = recs[i][0]
        elif recs[i][1] < rec4 and recs[i][1] >= rec5:  
            rec5 = recs[i][1]
            top5[4] = recs[i][0]

    #print("User: " + str(user))
    #print("Top 5: ")
    #print(top5)
    return top5

def report(estiDict):
    output = open(outFile, 'w')

    for users, recs in estiDict.items():
        output.write('%s' %users)
        for rec in recs:
            output.write(' ')
            output.write(str(rec[0]))
        output.write('\n') 



################################################################ Main ################################################################

def main():
    populateMovieDict(movieFile, movieDict)
    populateRatings(ratingFile, movieDict)
    populateMovieDict(movieFile, neighborDict)          #used for neighbor sets later
    #populateMovieDict(movieFile, estimateDict)          #used for rating estimations later
    populateActiveRatings(ratingFile, activeRatings)


    users = totalUsers(ratingFile, totalUserCount)
    centerAllScores(users, movieDict)


    #for i in range(len(movieDict)):
    #    addBlanks(users, movieDict, str(i + 1))

    #addBlanks(users, movieDict, '1')
    #print("Before:\n")
    #print(movieDict)

    for i in range(len(movieDict)):
       addBlanks(users, movieDict, str(i + 1))

    #print("\nAfter:\n")
    #print(movieDict)
    populateSimilarityDict(users, movieDict, similarityDict)
    #print("\nAfter:\n")
    #print(movieDict)
    #print(movieDict)

    #create a clean centered dictionary of movie ratings
    populateMovieDict(movieFile, movieDict)
    populateRatings(ratingFile, movieDict)
    #centerAllScores(users, movieDict)


    populateNeighborhood(neighborDict, similarityDict, movieDict)
    #print(neighborDict)

    #dotProducts(users, )

    #print("Movie Dictionary")
    #print(movieDict['1'])

    #print("Similarities")
    #print(similarityDict)

    #print(activeRatings)
    #estimateRating(similarityDict, neighborDict, movieDict, activeRatings, '3', '1')
    buildEsitDict(users, estimateDict)

    populateEstimates(users, similarityDict, neighborDict, movieDict, activeRatings, estimateDict)
    #print(estimateDict)

    #top5Recomemndations(estimateDict, 1)

    report(estimateDict)
    os.system('spd-say "your program has finished"')

    

if __name__ == "__main__":
    main()