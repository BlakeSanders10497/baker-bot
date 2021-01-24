import os.path
import matplotlib.pyplot as plt
import time
from os import path

import DatabaseOperations


def makeLeaderboard(leaderboardType, savePath):
    pointsList, nameList = getListData(leaderboardType)
 
    temp = 0
    tempName = ""

    #insertion sort algorithm
    for i in range(0, len(pointsList)):
        j = i
        
        while (j > 0 and pointsList[j] < pointsList[j - 1]): #if the number before the current number is lower, true
            temp = pointsList[j]
            tempName = nameList[j]

            #swap numeric values
            pointsList[j] = pointsList[j - 1]
            pointsList[j - 1] = temp

            #swap names so that the indicies of each list (name and points) match
            nameList[j] = nameList[j - 1]
            nameList[j - 1] = tempName
            
            j -= 1
            
        i += 1

    plt.style.use("ggplot")
    plt.cla() #clear plot so it doesnt overlap with previous plot
    
    value = []
    xLabel = ""
    logStatus = False
    if (leaderboardType == "bread"):
        for j in range(0, len(pointsList)):
            value.append(int(pointsList[j]))
        xLabel = "Bread"
        lbColor = 'blue'
        logStatus = True
    elif (leaderboardType == "gg wins"):
        for j in range(0, len(pointsList)):
            value.append(pointsList[j])
        xLabel = "Wins in Guessing Game"
        lbColor = 'red'
        logStatus = False
        
    x_pos = [i for i, _ in enumerate(nameList)]
    
    plt.barh(x_pos, value, color = lbColor, log = logStatus)
    plt.ylabel("Users")
    plt.xlabel(xLabel)
    plt.title("LEADERBOARD")
    plt.yticks(x_pos, nameList)
    plt.savefig(savePath, bbox_inches = 'tight', pad_inches = 0.1)
    




def getListData(leaderboardType):
    nameList = []
    pointsList = []

    with open('UserDatabase.txt', 'r') as file: #read the database file
        data = file.readlines()
    
    for count in range(0, len(data) - 1):
        userData = DatabaseOperations.convertToDict(data[count])
        if (int(userData[leaderboardType]) > 0): #if the user has at least 1 win or bread, count them in
            pointsList.append(int(userData[leaderboardType]))
            if (userData['nickname'] == ""):
                name = userData['name'][:-5]
            else:
                name = userData['nickname']
            nameList.append(name) #add name to list and splice the tag out (e.g. #1111)

    return pointsList, nameList


