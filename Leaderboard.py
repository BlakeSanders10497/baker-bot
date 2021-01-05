import os.path
import matplotlib.pyplot as plt
import time
from os import path

def leaderboard(folder, listFile, userFileExt, leaderboardType):
    completeName = os.path.join(folder, listFile)
    file = open(completeName, "r")
    userList = []
    userList = file.readline().split(',') #list of each user's name that has bread
    file.close()

    pointsList = getUserPointsList(userList, userFileExt) #list of each user's points

    temp = 0
    tempName = ""

    #insertion sort algorithm
    for i in range(0, len(userList)):
        j = i
        
        while (j > 0 and pointsList[j] < pointsList[j - 1]): #if the number before the current number is lower, true
            temp = pointsList[j]
            tempName = userList[j]

            #swap numeric values
            pointsList[j] = pointsList[j - 1]
            pointsList[j - 1] = temp

            #swap names so that the indicies of each list (name and points) match
            userList[j] = userList[j - 1]
            userList[j - 1] = tempName
            
            j -= 1
            
        i += 1


    plt.style.use("ggplot")
    
    breads = []
    xLabel = ""
    if (leaderboardType == "bread"):
        for j in range(0, len(pointsList)):
            breads.append(len(str(pointsList[j])) - 1)
        xLabel = "Amount of bread (10^x)"
        
    elif (leaderboardType == "guessing game"):
        for j in range(0, len(pointsList)):
            breads.append(pointsList[j])
        xLabel = "Wins in Guessing Game"   
    names = []
    for k in range(0, len(userList)):
        names.append(userList[k][:-5])

    x_pos = [i for i, _ in enumerate(names)]
    
    plt.barh(x_pos, breads, color = 'blue')
    plt.ylabel("Users")
    plt.xlabel(xLabel)
    plt.title("LEADERBOARD")
    plt.yticks(x_pos, names)
    plt.savefig('Other files/leaderboard.png', bbox_inches = 'tight', pad_inches = 0.1)
    
    return 'Other files/leaderboard.png'




def getUserPointsList(userList, userFileExt):
    userPointsList = []
    
    for count in range(0, len(userList)):
        userPath = os.path.join("User levels/", userList[count] + "" + userFileExt)
        checkIfFileExists(userPath)
        userFile = open(userPath, "r")
        userPoints = int(userFile.readline())
        userPointsList.append(userPoints)
        

    return userPointsList


def checkIfFileExists(pathName):
    exists = False
    if (not path.exists(pathName)):
        fileW = open(pathName, "w")
        fileW.write("0")
        fileW.close()
        
    else:
        exists = True

    return exists
