import time
from datetime import datetime
import random
import os.path

import DatabaseOperations


#get current time
def getTime():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    currTimeList = current_time.split(":")
    
    currTime = float(currTimeList[0])*60 + float(currTimeList[1])
    return currTime


#compare the current day, month, and year with the previous saved day/month/year
def checkDayMonthYear():
    datePath = os.path.join("Stats/", "date-save.txt")
    dateFile = open(datePath, "r")
    prevDateList = dateFile.readline().split(',')
    dateFile.close()
    
    canBake = False
    
    now = datetime.now()
    currDateList = str(now.strftime("%d,%m,%Y")).split(',')

    for i in range(0, len(currDateList) - 1):
        if (currDateList[i] > prevDateList[i]):
            canBake = True

    newDate = ",".join(currDateList)
    dateFile = open(datePath, "w")
    dateFile.write(newDate)
    dateFile.close()
    
    return canBake



#compare previous time and current time and make sure it has been at least the amount of time it is passed
def checkCooldown(user, cooldownType, cooldown): 
    userData = DatabaseOperations.getDataList(user)
    
    prevTime = float(userData[cooldownType]) 
    currTime = getTime()

    canBake = checkDayMonthYear()
    if (canBake): #if new day, month, or year, reset cooldowns/limits for everyone
        resetTime()
        
    if (currTime - float(prevTime) >= cooldown):
        canBake = True
    
        userData[cooldownType] = str(currTime) #update timeout to current time
        DatabaseOperations.writeToDB(userData)

    waitTime = cooldown - (float(currTime) - float(prevTime))
    
    return canBake, waitTime


#resets cooldowns and daily purchase limit because still havent fixed the damn time check function
def resetTime():
    with open('UserDatabase.txt', 'r') as file: #read the database file
        data = file.readlines()

    for i in range(0, len(data) - 1):
        userData = DatabaseOperations.convertToDict(data[i])
        userData['bread box purchases'] = '0'
        userData['gg cooldown'] = '-10'   #guess game cooldown
        userData['timeout'] = '-1'   #bake cooldown
        userData['citygame cooldown'] = '-15'
        userData['flaggame cooldown'] = '-10'
        userData['butter purchases'] = '0'
        userData['daily bakes'] = '0'
        
        DatabaseOperations.writeToDB(userData) #save to database file


#check how many times "test" has been called
def checkBakeCount(user):
    completeName = os.path.join("Stats/", "bake-count.txt")
    file = open(completeName, "r")
    count = int(file.readline())
    file.close()
    
    userData = DatabaseOperations.getDataList(user)
    
    bakesToday = userData['daily bakes']
    bakesTotal = userData['bakes']
    
    return f"```Today's bakes: {bakesToday}\nTotal bakes: {bakesTotal}\nAll user bakes combined: {count:,}```"



#returns how many times the gamble function has been called
def checkGambleCount():
    completeName = os.path.join("Stats/", "gamble-count.txt")
    file = open(completeName, "r")
    count = int(file.readline())
    file.close()
    return f"Gamble count: {count:,}"
    
    
#sets the user's nickname to the value they give. Used for trading, giving, and leaderboards
async def setNickname(user):
    msg = user.content.split()
    try:
        newName = " ".join(msg[1:])
    except:
        print("could not access msg[1] in setNickname")
        
    userData = DatabaseOperations.getDataList(user)

    oldName = userData['nickname']
    
    response = ""
    
    with open('UserDatabase.txt', 'r') as file: #read the database file
        data = file.readlines()
    
    for i in range(0, len(data) - 1):
        dbUser = DatabaseOperations.convertToDict(data[i])
        if (dbUser['nickname'] == newName):
            response = "another user already has that nickname"
        
    if (response == ""): #no user with that nickname was found
        userData['nickname'] = newName
        DatabaseOperations.writeToDB(userData)
        response = "<@" + userData['id'] + "> nickname changed from  **" + oldName + " ** to **" + newName + "**"

    await user.channel.send(response)


#returns the user's nickname if they have one
async def checkNickname(user):
    userData = DatabaseOperations.getDataList(user)

    if (userData['nickname'] == ""):
        response = "you have no set nickname, default is " + userData['name']
    else:
        response = "your nickname: " + userData['nickname']
        
    await user.channel.send(response)
