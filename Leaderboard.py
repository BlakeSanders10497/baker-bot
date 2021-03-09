import os.path
import matplotlib.pyplot as plt
import time
from os import path

import DatabaseOperations
import Utilities

def makeLeaderboard(leaderboardType, savePath):
    status = True
    pointsList, nameList = getListData(leaderboardType)
    
    if (len(nameList) == 0):
        print("nameList is empty after getListData() call in Leaderboard.py")
        status = False
        
    pointsList, nameList = lbSort(pointsList, nameList)
    

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
        
        if (value[-1] > 1000 and value[0] / value[-1] < 0.10): #if 1st place is over 1k and last place has less then 10% of 1st's bread, use log graph
            logStatus = True
        
    
        
    x_pos = [i for i, _ in enumerate(nameList)]
    
    plt.barh(x_pos, value, linewidth = 1, color = lbColor, log = logStatus, fill = True)
    plt.ylabel("Users")
    plt.xlabel(xLabel)
    plt.title("LEADERBOARD")
    plt.yticks(x_pos, nameList)
    plt.savefig(savePath, bbox_inches = 'tight', pad_inches = 0.1)
    
    return status


async def makeTextLB(leaderboardType):
    status = True
    pointsList, nameList = getListData(leaderboardType)
    pointsList, nameList = lbSort(pointsList, nameList)
    pointsList.reverse()
    nameList.reverse()
    
    leaderboard = "```css\n"
    
    for i in range(len(pointsList)):
        leaderboard += "\n." + str(i+1) + ") " + str(nameList[i]) + ": " + str(pointsList[i]) + "\n"
    
    leaderboard += "```"
    if (len(nameList) == 0):
        status = False
    
    if status == True:
        embed = await Utilities.getEmbedMsg(title_text = "LEADERBOARD", body_text = leaderboard)
    else:
        embed = await Utilities.getEmbedMsg(body_text = "```\nLeaderboard is empty due to lack of players on it```")
        
    return embed



def lbSort(pointsList, nameList):
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
    
    
    return pointsList, nameList



def getListData(leaderboardType):
    nameList = []
    pointsList = []

    data = DatabaseOperations.getDatabase()
    
    keys = list(data.keys())
    
    for id in keys:
        userData = data[id]
        if (userData[leaderboardType] > 0): #if the user has at least 1 win or bread, count them in
            pointsList.append(userData[leaderboardType])
            if (userData['nickname'] == ""):
                name = userData['name'][:-5]
            else:
                name = userData['nickname']
            nameList.append(name) #add name to list and splice the tag out (e.g. #1111)

    
    return pointsList, nameList


