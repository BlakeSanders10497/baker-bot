import discord
from discord.ext import commands
import asyncio
import random
import time
from datetime import datetime
import os.path
from os import path

bot = commands.Bot(command_prefix='.', description='A bot that greets the user back.')



broke = "<:Sadge:761225325723123732> you broke it (-1 points)"
notWorking = "<:pepelaugh:771033359837036564> not working (0 points)"
halfWorking = "<:ThinkingDank:385065840418095115> half working (1 point)"
working = "<:PogU:771737926936559656> working (2 points)"
reallyWorking = "<:FeelsAmazingMan:400752334856126465> really working (4 points)"
fixed = "<:5Head:771067313738481674> improved it (7 points)"
stonks = "<:stonks:761227625423044629> STONKS (50 points)"

timeList = []
msg = []
responses = ["<:Sadge:761225325723123732> oven not working", "<:Sadge:761225325723123732> oven not working",
             "<:Sadge:761225325723123732> oven not working", "<:Sadge:761225325723123732> oven not working",
             "<:Sadge:761225325723123732> oven not working", "<:pepelaugh:771033359837036564> undercooked",
             "<:pepelaugh:771033359837036564> undercooked", "<:pepelaugh:771033359837036564> undercooked",
             "<:pepelaugh:771033359837036564> undercooked", "<:pepelaugh:771033359837036564> undercooked",
             "<:ThinkingDank:385065840418095115> not enough butter", "<:ThinkingDank:385065840418095115> not enough butter",
             "<:ThinkingDank:385065840418095115> not enough butter", "<:ThinkingDank:385065840418095115> not enough butter",
             "<:ThinkingDank:385065840418095115> needs more baking powder", "<:ThinkingDank:385065840418095115> needs more baking powder",
             "<:ThinkingDank:385065840418095115> needs more baking powder", 
             "<:PogU:771737926936559656> cooked nicely",
             "<:PogU:771737926936559656> cooked nicely", "<:PogU:771737926936559656> cooked nicely",
             "<:PogU:771737926936559656> cooked nicely", "<:PogU:771737926936559656> cooked nicely",
             "<:PogU:771737926936559656> cooked nicely",
             "<:peepofat:775341285544427561> crisp bread", "<:peepofat:775341285544427561> crisp bread", "<:peepofat:775341285544427561> crisp bread",
             "<:FeelsAmazingMan:400752334856126465> cooked to perfection", "<:FeelsAmazingMan:400752334856126465> cooked to perfection",
             "<:stonks:761227625423044629> gordon ramsey of baking"]




async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')



#after saying test in chat, the function picks a random response from the list above and awards the user those points
def testRand(userName):
    
    completeName = os.path.join("User levels/", userName + ".txt")
    
    checkIfExists(completeName) #make sure user already has a file
    
    
    file = open(completeName, "r")
    points = file.readline() #read user's points
    file.close()

    if (int(points) < 1000): #if users points are below 10000, stick to normal point giving system, if not, then it uses percentages 
        num = int(random.random()*len(responses)) #random number between 0 and # of responses
        status = responses[num] + " (" + str(num) + " bread)"
        reward = num
    else:
        percent = random.randrange(1, 41) / 1000 #get a number between 0.001 and 0.02
        print(percent)
        if (percent >= 0.039):
            num = 28
            reward = int(points) * 0.25 #Special reward that gives 10% if the random percent is 2%
            percent = 0.25
        else:
            if (percent >= 0.03):
                num = int(random.randrange(23, 28))
            elif (percent >= 0.015 and percent < 0.030):
                num = int(random.randrange(10, 22))
            else:
                num = int(random.randrange(0, 9))
            reward = int(points) * percent #get the percent of the user's points
        status = responses[num] + " (+{:,} bread, ".format(int(reward)) + "{:.2f}".format(percent * 100) + "%)"
        
    
                  
    file = open(completeName, "w")
    file.write(str(int(points) + int(reward))) #write updated user's points
    file.close()
    
    completeName = os.path.join("Other files/", "test count.txt")
    file = open(completeName, "r")
    count = int(file.readline())
    count += 1 #increase test count
    file.close()
    file = open(completeName, "w")
    file.write(str(count))
    file.close()
    
    return status



#a user enters the amount they want to gamble, and the function randomly choses a number in the resultList and multiplies the 
#  amount the bet by that number and adds it to the user's total points. e.g.: if number chosen is -1, points (5) * -1 = -5,
#    points (5) + -5 = 0
def gamble(userName, amount):
    completeName = os.path.join("User levels/", userName + ".txt")
    checkIfExists(completeName)
    resultList = [-1, -1, -1, -1, 0, 1, 1, 1, 1, 2] 
    
    file = open(completeName, 'r')
    points = int(file.readline())
    if (points <= 0):
        response = "you're too broke to gamble <:Sadge:761225325723123732>"
    elif (int(amount) > points):
        response = "you can't bet more than you have <:Weird:568458482840502302>"
    else:
        num = int(random.random()*10)
        value = int(amount) * resultList[num]
        points += value
        #print(points)
        #print(num)
        file = open(completeName, 'w')
        file.write(str(points))
        file.close()
        
        if (num <= 3):
            response = "You lost {:,} bread".format(value)
        elif (num == 4):
            response = "You didn't gain or lose any bread"
        elif (num >= 5):
            response = "You gained {:,} bread".format(value)

        completeName = os.path.join("Other files/", "gamble count.txt")
        file2 = open(completeName, "r")
        count = int(file2.readline()) #extract gamble count value
        count += 1 #increase it
        file2.close()
        file2 = open(completeName, "w")
        file2.write(str(count)) #send new gamble count back in
        file2.close()
        
    return response


#returns how many times the gamble function has been called
def checkGambleCount():
    completeName = os.path.join("Other files/", "gamble count.txt")
    file = open(completeName, "r")
    count = int(file.readline())
    file.close()
    return f"Gamble count: {count:,}"



#check if a user's point file exists, if not, create one with 0 points
def checkIfExists(completeName):
    exists = True
    if (not path.exists(completeName)):
        file = open(completeName, "w")
        file.write("0")
        file.close()
        exists = False
        completeNameTimeout = completeName[:-4] + " Timeout.txt"
        print(completeNameTimeout)
        fileTimeout = open(completeNameTimeout, "w")
        fileTimeout.write("0")
        fileTimeout.close()
        
        completeName2 = os.path.join("User levels/", ",List of Account names.txt")     
        file2R = open(completeName2, "r")
        userList = file2R.readline().split(',')
        #print("userl")
        print(userList)
        file2R.close()
        userName = completeName[12:-4] #cut out User levels/  and  .txt
        newUserList = ""

        #list of usernames needs to be one line comma-separated
        for count in range(0, len(userList)):
            newUserList = "," + newUserList + userList[count]
            
        print(userName)
        newUserList += userName #add username to end of list
        
        file2W = open(completeName2, "w")
        file2W.write(str(newUserList))
        file2W.close()
    return exists



#check how many times "test" has been called
def checkTestCount():
    completeName = os.path.join("Other files/", "test count.txt")
    file = open(completeName, "r")
    count = file.readline()
    file.close()
    return "Bakes completed: " + count 




#check how many points a user has
def checkLevel(userName):
    completeName = os.path.join("User levels/", userName + ".txt")

    checkIfExists(completeName)
    
    file = open(completeName, "r")
    level = int(file.readline())
    #response = f"{level:,}"
    return f"{level:,} loaves of bread"




#timer #TODO setting the timer halts the whole program, make it not do that
def custTimer(x):
    time.sleep(int(x))
    return 'lobby is scheduled now!'





#get current time
def getTime():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    currTimeList = current_time.split(":")
    
    currTime = float(currTimeList[0])*60 + float(currTimeList[1])
    return currTime


#compare previous time and current time and make sure it has been at least 1 minute
def checkTime(userName):
    fUserName = "User levels/" + str(userName) + ".txt"
    checkIfExists(fUserName)
    
    prevTime = getPrevTime(userName) #returns a string with time
    currTime = getTime()

    canTest = False 
    
    if (currTime - float(prevTime) > 0.5): #if current time is greater than previous time by more than 0.5 minutes
        canTest = True
    
    completeName = os.path.join("User levels/", str(userName) + " Timeout.txt")
    file = open(completeName, "w")
    file.write(str(currTime)) #send the current time because it is now the previous time\
    file.close()
    
    return canTest










#retrieve the time that the author last said test
def getPrevTime(userName):
    completeName = os.path.join("User levels/", str(userName) + " Timeout.txt")

    file = open(completeName, "r")
    prevTime = file.readline()
    file.close()

    return prevTime




#sets the timeout to 0 because still havent fixed the damn time check function
def resetTime():
    completeName = os.path.join("User levels/", ",List of Account names.txt")
    file = open(completeName, "r")
    userList = []
    userList = file.readline().split(',') #split the line of acc names and put in list
    file.close()
    
    for count in range(0, len(userList)):
        timeoutPathName = os.path.join("User levels/", userList[count] + " Timeout.txt")
        file2 = open(timeoutPathName, "w")
        file2.write("-1")
        file2.close()

        boxPurchasesPath = os.path.join("User levels/", userList[count] + " Bread box Purchases.txt")
        filePurchases = open(boxPurchasesPath, "w")
        filePurchases.write("0")
        filePurchases.close()

        pathName = os.path.join("User levels/", userList[count] + " guess game cooldown.txt")
        cooldownFile = open(pathName, "w")
        cooldownFile.write("-10")
        cooldownFile.close()
        




#get user points and place them in a list
def getUserPointsList(userList):
    userPointsList = []
    
    for count in range(0, len(userList)):
        userPath = os.path.join("User levels/", userList[count] + ".txt")
        userFile = open(userPath, "r")
        userPoints = int(userFile.readline())
        userPointsList.append(userPoints)

    return userPointsList



#posts all accounts and their points in 1 message
def leaderboard():
    completeName = os.path.join("User levels/", ",List of Account names.txt")
    file = open(completeName, "r")
    userList = []
    userList = file.readline().split(',') #list of each user's name that has bread
    file.close()
    #print("user list:")
    #print(userList)
    leaderboard = "```css\n\t\t\t\t\t\t\t LEADERBOARD\n\n"
    
    pointsList = getUserPointsList(userList) #list of each user's points
    #print(pointsList)
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

    
    count = 0
    rank = 1
    currentUser = len(userList) - 1
    while (count < len(userList)):
        
        if (pointsList[currentUser] > 100000000000000000): #if the user is above 100 quadrillion, use scientific notation
            points = str(pointsList[currentUser])
            sciNotation = points[0] + "." + str(points[1] + points[2]) + "x10^" + str(len(points) - 1) 
            leaderboard = leaderboard + "." + str(rank) + ") " + userList[currentUser][:-5] + " : " + sciNotation + "\n\n"
        else:
            leaderboard = leaderboard + "." + str(rank) + ") " + userList[currentUser][:-5] + " : " + f"{pointsList[currentUser]:,}" + "\n\n"
        count += 1
        rank += 1
        currentUser -= 1
        
    leaderboard += "\n```"
    
    return leaderboard




def checkBreadBoxPath(user):
    exists = False
    userBreadBoxPath = os.path.join("User levels/", user + " Bread box.txt")
    if (not path.exists(userBreadBoxPath)):
        fileW0 = open(userBreadBoxPath, "w")
        fileW0.write("0")
        exists = True  
    
    return exists



def maxBreadBoxPurchases(user):
    reachedLimit = False
    boxPurchasesPath = os.path.join("User levels/", user + " Bread box Purchases.txt")
    if (not path.exists(boxPurchasesPath)):
        fileW0 = open(boxPurchasesPath, "w")
        fileW0.write("0")
        fileW0.close()
    else:
        fileR = open(boxPurchasesPath, "r")
        if (int(fileR.readline()) >= 15):
            reachedLimit = True
        fileR.close()

    return reachedLimit




def getBoxPurchases(user):
    boxPurchasesPath = os.path.join("User levels/", user + " Bread box Purchases.txt")
    file = open(boxPurchasesPath, "r")
    boxPurchases = 15 - int(file.readline())
    
    return "You have " + str(boxPurchases) + " boxes left to buy today"



#check if user being traded or donated to exists (or if there is any duplicates)
def checkName(user):
    nameListPath = os.path.join("User levels/", ",List of Account names.txt")
    file = open(nameListPath, "r")
    userList = []
    userList = file.readline().split(',')
    count = 0
    match = 0

    name = ""
    
    for count in range(0, len(userList)):
        if (str(user) == userList[count][:-5]):
            match += 1
            name = userList[count]
            #print(name)
        count += 1
        
    if (match > 1):
        name = "duplicate"

    return name



    


#takes X bread from the author and gives specified user X bread 
def giveBread(donator, user, breadAmountRaw):
    response = ""
    completeName = os.path.join("User levels/", donator + ".txt")
    checkIfExists(completeName)
    file = open(completeName, "r")
    donatorPoints = int(file.readline())

    breadAmount = int("".join(breadAmountRaw.split(",")))
    #print(user)
    user = checkName(user)

    if (user == "duplicate"):
        response = "Error: there are more than 1 accounts with that name"
    else:
        if (breadAmount <= donatorPoints and breadAmount >= 0):
            #get points of the person being given bread
            completeName = os.path.join("User levels/", user + ".txt")
            fileUser = open(completeName, "r")
            userPoints = int(fileUser.readline())
            fileUser.close()

            #add the donated amount to their points
            userPoints += int(breadAmount)
            fileUserW = open(completeName, "w")
            fileUserW.write(str(userPoints))
            fileUserW.close()

            #subtract the donated amount from the donators point total
            completeName = os.path.join("User levels/", donator + ".txt")
            file = open(completeName, "r")
            donatorPoints = int(file.readline()) #reading donator points again in case the author is donating to themself
            donatorPoints -= int(breadAmount)
            file.close()
        
            fileDonatorW = open(completeName, "w")
            fileDonatorW.write(str(donatorPoints))
            fileDonatorW.close()

            response = "donated {:,} bread to {} :)".format(breadAmount, user[:-5])
        
        else:
            response = "you can't donate more bread than you have <:Weird:568458482840502302>"

    
    return response



                                                                                        # STORE FUNCTIONS

def store(user):
    completeName = os.path.join("User levels/", user + ".txt")
    checkIfExists(completeName)
    file = open(completeName, "r")
    userPoints = int(file.readline())
    output = ""
    
    if (userPoints < 100):
        output = "you need at least 100 bread to shop at the store"
    else:
        relativePrice = int(userPoints * 0.1)
        output = "```\t\t\tSTORE\n\n\tITEM\t\t\tPrice\n\n A1) Bread Box - ({:,}".format(relativePrice) + " bread)```"

    
    return output

        
    
def storePurchase(user, item):
    completeName = os.path.join("User levels/", user + ".txt")
    checkIfExists(completeName)
    file = open(completeName, "r")
    userPoints = int(file.readline())
    file.close()
    output = ""
    
    if (userPoints < 100):
        output = "you need at least 100 bread to shop at the store"
    else:

        if (item == "A1"):

            if (not maxBreadBoxPurchases(user)):
            
                relativePrice = int(userPoints * 0.1)
                userPoints -= relativePrice

                userBreadBoxPath = os.path.join("User levels/", user + " Bread box.txt")
                userPurchaseBoxPath = os.path.join("User levels/", user + " Bread box Purchases.txt")
                if (not path.exists(userBreadBoxPath)):
                    fileW0 = open(userBreadBoxPath, "w")
                    fileW0.write("1")
                    
                    fileW1 = open(userPurchaseBoxPath, "w")
                    fileW1.write("1")
                else:
                    fileBreadBoxR = open(userBreadBoxPath, "r")
                    breadBoxCount = int(fileBreadBoxR.readline())
                    fileBreadBoxR.close()

                    breadBoxCount += 1

                    fileBreadBoxW = open(userBreadBoxPath, "w")
                    fileBreadBoxW.write(str(breadBoxCount))
                    fileBreadBoxW.close()
                    
                    
                    fileBoxPurchasesR = open(userPurchaseBoxPath, "r")
                    BoxPurchaseCount = int(fileBoxPurchasesR.readline())
                    fileBoxPurchasesR.close() #close read file  
                    
                    BoxPurchaseCount += 1
                    
                    fileBoxPurchasesW = open(userPurchaseBoxPath, "w")
                    fileBoxPurchasesW.write(str(BoxPurchaseCount))
                    fileBoxPurchasesW.close()
        
                fileW2 = open(completeName, "w")
                fileW2.write(str(userPoints))

                output = "Purchased 1 bread box (-{:,}".format(relativePrice) + ")"
            else:
                output = "you have reached your bread box daily limit"

                
    return output




                                                                                       # BREAD BOX FUNCTIONS

def openBreadBox(user):
    completeName = os.path.join("User levels/", user + ".txt")
    checkIfExists(completeName)
    file = open(completeName, "r")
    userPoints = int(file.readline())
    file.close()
    output = ""

    userBreadBoxPath = os.path.join("User levels/", user + " Bread box.txt")
    checkBreadBoxPath(user)

    fileBreadBoxR = open(userBreadBoxPath, "r")
    userBoxes = int(fileBreadBoxR.readline())
    fileBreadBoxR.close()
    
    if (userBoxes < 1):
        output = "you dont have any bread boxes to open"
    else:
        percent = random.randrange(1, 51) / 100
        reward = userPoints * percent
        
        userPoints += int(reward) #add reward amount to total points
        userBoxes -= 1 #remove 1 box
        
        fileBreadBoxW = open(userBreadBoxPath, "w")
        fileBreadBoxW.write(str(userBoxes))
        fileBreadBoxW.close()

        fileUserPointsW = open(completeName, "w")
        fileUserPointsW.write(str(userPoints))
        fileUserPointsW.close()


        if (percent <= 0.1):
            output = "Bread box gave you {:,}".format(int(reward)) + " bread <:FeelsBadMan:303787556213096458>" + " ({:.2f}".format(percent * 100) + "%)"
        if (percent > 0.1 and percent <= 0.25):
            output = "Bread box gave you {:,}".format(int(reward)) + " bread <:FeelsGoodMan:452068213665300490>" + " ({:.2f}".format(percent * 100) + "%)"
        if (percent > 0.25):
            output = "Bread box gave you {:,}".format(int(reward)) + " bread <:PogU:771737926936559656>" + " ({:.2f}".format(percent * 100) + "%)"

    return output
    



def tradeBox(donator, user, amount):
    response = ""
    completeName = os.path.join("User levels/", donator + " Bread box.txt")
    checkIfExists(completeName)
    file = open(completeName, "r")
    donatorBoxes = int(file.readline())

    user = checkName(user)
    if (user == "duplicate"):
        response = "Error: there are more than 1 accounts with that name"
    else:
        if (int(amount) > donatorBoxes):
            response = "you cant donate more than you have <:Weird:568458482840502302>"
        else:
            donatorBoxes -= int(amount)
            fileDonatorW = open(completeName, "w")
            fileDonatorW.write(str(donatorBoxes))
            fileDonatorW.close()

            userBoxPath = os.path.join("User levels/", user + " Bread box.txt")
            checkBreadBoxPath(user)
            fileUserR = open(userBoxPath, "r")
            userBoxes = int(fileUserR.readline())
            fileUserR.close()

            userBoxes += int(amount)

            fileUserW = open(userBoxPath, "w")
            fileUserW.write(str(userBoxes))
            fileUserW.close()
        
            response = "donated " + str(amount) + " bread boxes to " + str(user)[:-5] + " :)"

    return response

def getBreadBoxCount(user):
    userBreadBoxPath = os.path.join("User levels/", user + " Bread box.txt")
    checkBreadBoxPath(user)
    output = ""
    
    fileBreadBoxR = open(userBreadBoxPath, "r")
    userBoxes = int(fileBreadBoxR.readline())
    fileBreadBoxR.close()

    if (userBoxes == 0):
        output = "You have no bread boxes"
    if (userBoxes == 1):
        output = "You have " + str(userBoxes) + " bread box"
    if (userBoxes > 1):
        output = "You have " + str(userBoxes) + " bread boxes"


    return output




                                                                                        # LOTTERY FUNCTIONS
def checkIfUserPredict(completeName):
    exists = True
    if (not path.exists(completeName)):
        file = open(completeName, "w")
        file.write("0")
        file.close()
        exists = False
    return exists


def checkUserTicketFile(completeName):
    exists = True
    if (not path.exists(completeName)):
        file = open(completeName, "w")
        file.write("")
        file.close()
        exists = False
    return exists


def checkJackpot():
    jackpotPath = os.path.join("Other files/", "Jackpot.txt")
    checkIfUserPredict(jackpotPath)
    currentPotFile = open(jackpotPath, "r")
    pot = int(currentPotFile.readline())
    currentPotFile.close()

    return "Current jackpot: " + str(pot) + " bread boxes"


def lotteryPredictions():
    activePredictions = os.path.join("Other files/", "Active Lottery.txt")
    checkIfUserPredict(activePredictions)
    
    
    fileActivePrediction = open(activePredictions, "r")
    active = fileActivePrediction.readline()
    fileActivePrediction.close()
    
    if (active == "false"):
        fileActivePredictionW = open(activePredictions, "w")
        fileActivePredictionW.write("true")        
        fileActivePredictionW.close()

    nameListPath = os.path.join("User levels/", ",List of Account names.txt")
    file = open(nameListPath, "r")
    userList = []
    userList = file.readline().split(',')

    #set the current donations to 10 for everyone so there is a minimum of 1 guess per person (without donating)
    for count in range(0, len(userList)):
        path = os.path.join("User levels/", userList[count] + " current donations.txt")
        guessAvailFileR = open(path, "r")
        totalGuesses = int(guessAvailFileR.readline())

        totalGuesses += 10
        
        guessAvailFile = open(path, "w")
        guessAvailFile.write(str(totalGuesses))
        guessAvailFile.close()
    
    return "predictions are active"
    

def getDonationsConversion(path):
    currentDonationsFile = open(path, "r")
    totalDonations = int(currentDonationsFile.readline())
    currentDonationsFile.close()

    count = 0
    tempTotal = totalDonations
    while (tempTotal > 1):
        tempTotal -= 10
        count += 1

    return count
    


def getGuessCount(user):
    path = os.path.join("User levels/", user + " current donations.txt")
    guesses = getDonationsConversion(path)

    return "Available guesses: " + str(guesses)



def checkTickets():
    activePredictions = os.path.join("Other files/", "Active Lottery.txt")
    file = open(activePredictions, "r")
    active = file.readline()
    ticketsList = ""
    
    if (active == "true"):
        userList = []
        with open("Other files/Users in lottery.txt") as f:
            userList = f.readline().split(",")
    
        ticketsList = "```css\n\t\t\t\t\tTICKETS\n"

       
        for count in range(0, len(userList) - 1):
            count += 1 #skip the first comma 
            completeName2 = os.path.join("User levels/", userList[count] + " lottery guess.txt")
            file2 = open(completeName2, "r")
            userGuesses = file2.readline()

            ticketsList += "\n" + str(userList[count][:-5]) + ": " + userGuesses[1:]
            

        ticketsList += "\n```"
    else:
        ticketsList = "there are no tickets right now"

    return ticketsList






def userPredict(user, userGuess):
    activePredictions = os.path.join("Other files/", "Active Lottery.txt")
    fileActivePrediction = open(activePredictions, "r")
    active = fileActivePrediction.readline()
    fileActivePrediction.close()
    
    response = ""
    
    if (active == "false"):
        response = "Lottery is not active right now :)"
    elif (active == "true"):
        userGuessPath = os.path.join("User levels/", user + " lottery guess.txt")
        checkUserTicketFile(userGuessPath)

        if (int(userGuess) > 0 and int(userGuess) <= 200):

            completeName = os.path.join("User levels/", user + ".txt")
            checkIfExists(completeName)
            
            #check how much bread user has
            userBreadFile = open(completeName, "r")
            userPoints = int(userBreadFile.readline())
            userBreadFile.close()

            cost = 0

            donatePath = os.path.join("User levels/", user + " current donations.txt")
            checkIfUserPredict(donatePath)
            guessesAvailable = getDonationsConversion(donatePath)

            if (guessesAvailable <= 0):
                response = "you dont have any guesses remaining (donate to get more; 11 guesses max)"
            else:
                if (userPoints > 0):
                    if (userPoints < 10000): #cost is 1 bread for anyone less than 10k bread
                        cost = 1
                    elif (userPoints >= 10000): #cost is 0.01% of user's total bread for anyone above 10k bread
                        cost = userPoints * 0.0001

                    #update player points
                    newUserBreadFile = open(completeName, "w")
                    newUserBreadFile.write(str(int(userPoints - cost)))
                    newUserBreadFile.close()

                    #save user's guess
                    userGuessFileW = open(userGuessPath, "r")
                    totalGuesses = userGuessFileW.readline() #this is a line of integers (195,34,48,155,...)
                    userGuessFileW.close()
                    
                    updatedTotalGuesses = totalGuesses + "," + userGuess
                    
                    userGuessFile = open(userGuessPath, "w")
                    userGuessFile.write(updatedTotalGuesses)
                    userGuessFile.close()
                    
                    response = str(user)[:-5] + " has entered " + str(userGuess) + " as their lottery ticket " + "(cost: {:,} bread".format(int(cost)) + ")"

                    #check if user is already in the list of participants 
                    predictionPath = os.path.join("Other files/", "Users in lottery.txt")
                    predictionFile = open(predictionPath, "r")
                    users = predictionFile.readline()
                    userList = users.split(",")
                    
                    participating = False
                    for count in range(0, len(userList) - 1):
                        count += 1
                        if (str(user) == str(userList[count])):
                            participating = True

                    if (not participating):
                        #add user to list of participants 
                        newPredictionFile = open(predictionPath, "w")
                        newPredictionFile.write(users + "," + user)
                        newPredictionFile.close()
            
                    #add 7 bread boxes for each user that enters
                    jackpotPath = os.path.join("Other files/", "Jackpot.txt")
                    checkIfUserPredict(jackpotPath)
                    currentPotFile = open(jackpotPath, "r")
                    pot = int(currentPotFile.readline())
                    currentPotFile.close()
                
                    newPot = pot + 7

                    newPotFile = open(jackpotPath, "w")
                    newPotFile.write(str(newPot))
                    newPotFile.close()

                    #reduce the number of guesses available
                    guessPath = os.path.join("User levels/", user + " current donations.txt")
                    checkIfUserPredict(guessPath)
                    guessesFile = open(guessPath, "r")
                    guesses = int(guessesFile.readline())
                    guessesFile.close()

                    guesses -= 10
                    
                    updatedGuessFile = open(guessPath, "w")
                    updatedGuessFile.write(str(guesses))
                    updatedGuessFile.close()
                    
     
        else:
            response = "your number is out of range, choose a number between 1 and 200"
                       
    return response




def donateToJackpot(user, donation):
    response = ""
    guessPath = os.path.join("User levels/", user + " number of guesses.txt")
    checkIfUserPredict(guessPath)
    totalGuessesFile = open(guessPath, "r")
    totalGuesses = int(totalGuessesFile.readline())
    totalGuessesFile.close()

    if (totalGuesses >= 11):
        response = "you have donated the max amount already"
    else:
        if (int(donation) < 1):
            response = "<:WeirdChamp:778827632053583872> you can't donate less than 1%"
        elif (int(donation) > 100):
            response = "<:WeirdChamp:778827632053583872> you can't donate more than 100% of your bread"
        else:
            completeName = os.path.join("User levels/", user + ".txt")
            checkIfExists(completeName)
            
            #check how much bread user has
            userBreadFile = open(completeName, "r")
            userBread = int(userBreadFile.readline())
            userBreadFile.close()
        
            percentAmnt = int(userBread * (int(donation)/100)) #get the bread value of the % of their total
            userBread = int(userBread - percentAmnt) #subtract what they donated from their total bread
        
            #write new bread amount
            breadFile = open(completeName, "w")
            breadFile.write(str(userBread))
            breadFile.close()
        
            breadBoxValue = int(donation) * 2 #bread box value is 2x the percent they donate. open to change
        
            #add boxes to jackpot
            jackpotPath = os.path.join("Other files/", "Jackpot.txt")
            checkIfUserPredict(jackpotPath)
            currentPotFile = open(jackpotPath, "r")
            pot = int(currentPotFile.readline())
            currentPotFile.close()
        
            newPotFile = open(jackpotPath, "w")
            newPotFile.write(str(pot + breadBoxValue))
            newPotFile.close()

            #save the amount they donated so it increases their chances in winning the lottery
            donatePath = os.path.join("User levels/", user + " current donations.txt")
            checkIfUserPredict(donatePath)
            currentDonationsFile = open(donatePath, "r")
            totalDonations = int(currentDonationsFile.readline())
            currentDonationsFile.close()

            if (totalDonations < 100): #limit is 10 guesses, dont add more if its above 10
                totalDonations += int(donation)

                newDonationsFile = open(donatePath, "w")
                newDonationsFile.write(str(totalDonations))
                newDonationsFile.close()

            totalGuesses += 1
            totalGuessesFileW = open(guessPath, "w")
            totalGuessesFileW.write(str(totalGuesses))
            totalGuessesFileW.close()
                

            response = "<:PogChamp:304416481528250369> " + user[:-5] + " donated " + str(breadBoxValue) + " bread boxes to the jackpot\nCost: -{:,} bread".format(int(percentAmnt))

    return response




def stopLottery():
    activePredictions = os.path.join("Other files/", "Active Lottery.txt")
    file = open(activePredictions, "r")
    active = file.readline()

    response = ""
    
    if (active == "false"):
        response = "predicts are already inactive"
    else:
        file = open(activePredictions, "w")
        file.write("false")
        file.close()
        
        response = "predictions have closed"

        
    return response


    
def startLottery():
    activePredictions = os.path.join("Other files/", "Active Lottery.txt")
    file = open(activePredictions, "r")
    active = file.readline()
    file.close()
    response = ""
    if (active == "false"):
        response = "lottery is not active right now"
    elif (active == "true"):
        
        
        userList = []
        with open("Other files/Users in lottery.txt") as f:
            userList = f.readline().split(",")
            
        print("lottery user list:")
        print(userList)
        
        lotteryNum = random.randrange(1, 201) #jackpot number
        print("lott: " + str(lotteryNum))
        winner = ""
        count = 0
        
        for count in range(0, len(userList) - 1):
            count += 1
            print(userList[count])
            completeName2 = os.path.join("User levels/", userList[count] + " lottery guess.txt")
            file2 = open(completeName2, "r")
            userGuesses = file2.readline().split(",")
            file2.close()
            i = 0

            for i in range(0, len(userGuesses) - 1):
                i += 1
                #print(userGuesses[i])
                
                if (int(userGuesses[i]) == lotteryNum):
                    #print("win")
                    #print("count: " + str(count))
                    #get jackpot amount
                    jackpotPath = os.path.join("Other files/", "Jackpot.txt")
                    checkIfUserPredict(jackpotPath)
                    currentPotFile = open(jackpotPath, "r")
                    pot = int(currentPotFile.readline())
                
                    winner = userList[count]
                    response = "<:PogU:771737926936559656> " + str(userList[count][:-5]).upper() + " WON THE LOTTERY!!! (Winning number: " + str(lotteryNum) + ")\nPrize: " + str(pot) + " bread boxes"                           

                    #retreive winner's boxes 
                    userBreadBoxPath = os.path.join("User levels/", userList[count] + " Bread box.txt")
                    checkBreadBoxPath(userList[count])
                    fileBreadBoxR = open(userBreadBoxPath, "r")
                    userBoxes = int(fileBreadBoxR.readline())
                    fileBreadBoxR.close()

                    userBoxes += pot

                    #save new bread box count to user's inventory
                    fileBreadBoxW = open(userBreadBoxPath, "w")
                    fileBreadBoxW.write(str(userBoxes))
                    fileBreadBoxW.close()

                    #set jackpot to 0
                    resetJackpot = open(jackpotPath, "w")
                    resetJackpot.write("0")
                    resetJackpot.close()

                i += 1
                
            count += 1

        if (winner == ""):
            response = "<:Sadge:761225325723123732> nobody guessed the winning number (" + str(lotteryNum) + ")"

        #clear names from prediction list so that it's ready for next lottery
        userPredList = os.path.join("Other files/", "Users in lottery.txt")
        wipePredList = open(userPredList, "w")
        wipePredList.write("")
        wipePredList.close()
    
        for j in range(0, len(userList)):
            ticketPath = os.path.join("User levels/", userList[j] + " lottery guess.txt")
            ticketFile = open(ticketPath, "w")
            ticketFile.write("")
            ticketFile.close()

            donatePath = os.path.join("User levels/", userList[j] + " current donations.txt")
            checkIfUserPredict(donatePath)
            currentDonationsFile = open(donatePath, "w")
            currentDonationsFile.write("0")
            currentDonationsFile.close()

        
    #set lottery status to inactive
    lotteryFile = open(activePredictions, "w")
    lotteryFile.write("false")
    lotteryFile.close()

    
    return response






                                                                                # GUESSING GAME FUNCTIONS

# check if a user can play the guess game or not, returns true or false
def checkGuessGameCooldown(userName):
    prevTime = getPrevGuessGameTime(userName) #returns a string with time
    currTime = getTime()

    canPlay = False 
    
    if (float(currTime) - float(prevTime) >= 10): #if current time is greater than previous time by more than 5 minutes
        canPlay = True
        
    return canPlay


#retrieve the previous time a user played the guessing game
def getPrevGuessGameTime(userName):
    pathName = os.path.join("User levels/", userName + " guess game cooldown.txt")
    
    if (not path.exists(pathName)):
        fileW = open(pathName, "w")
        fileW.write("0")
        fileW.close()
        prevTime = 0
    else:
        fileR = open(pathName, "r")
        prevTime = float(fileR.readline())
    
    
    return prevTime



def checkIfGuessGameActive(statusPath):
    if (not path.exists(statusPath)):
        gameActivate = open(statusPath, "w")
        gameActivate.write("false")
        gameActivate.close()
        status = "false"
    else:
        gameActive = open(statusPath, "r")
        status = gameActive.readline()
        gameActive.close()

    return status
    
    

def startGuessGame(user):
    response = ""
    userGuessPath = os.path.join("User levels/", user + " guess game status.txt")
    status = checkIfGuessGameActive(userGuessPath)

    canPlay = checkGuessGameCooldown(user)
    
    if (status == "true"):
        response = "Guessing game is already active for " + user[:-5]
    elif (not canPlay):
        prevTime = getPrevGuessGameTime(user)
        currTime = getTime()
        waitTime = 10 - (float(currTime) - float(prevTime))
        if (waitTime > 1):
            response = "Cooldown is active. Wait time is " + str(waitTime)[:-2] + " minutes"
        else:
            response = "Cooldown is active. Wait time is " + str(waitTime)[:-2] + " minute"
    else:
        #set game status to true
        gameActivate = open(userGuessPath, "w")
        gameActivate.write("true")
        gameActivate.close()

        #pick a number between 1 and 20 for the user to guess
        computerNumPath = os.path.join("User levels/", user + " guess game winning number.txt")
        numberFile = open(computerNumPath, "w")
        winNumber = random.randrange(1, 16)
        numberFile.write(str(winNumber))
        numberFile.close()

        #set available guesses to default (3)
        availableGuessPath = os.path.join("User levels/", user + " guess game available guesses.txt")
        availGuessFile = open(availableGuessPath, "w")
        availGuessFile.write(str(3))
        availGuessFile.close()

        response = "Guessing game has started for " + str(user)[:-5] + ". Pick a number between 1 and 15"
        
    return response


#retrieve the number of available guesses a user has
def getAvailableGuesses(user):
    availableGuessPath = os.path.join("User levels/", user + " guess game available guesses.txt")
    availGuessFile = open(availableGuessPath, "r")
    availGuesses = int(availGuessFile.readline())
    availGuessFile.close()
    
    return availGuesses



def readGuess(user, guess):
    guessStatusPath1 = os.path.join("User levels/", user + " guess game status.txt")
    status = checkIfGuessGameActive(guessStatusPath1)
    output = ""
    
    if (status != "true"):
        output = "guessing game is not active (do !start guessing first)"
    elif (int(guess) > 15 or int(guess) < 1):
        output = "guess out of bounds. select a number between 1 and 15"
    else:
        computerNumPath = os.path.join("User levels/", user + " guess game winning number.txt")
        winFile = open(computerNumPath, "r")
        winningNum = int(winFile.readline())
        winFile.close()

        if (guess == winningNum):
            userBreadBoxPath = os.path.join("User levels/", user + " Bread box.txt")
            checkBreadBoxPath(user)
            output = "<:PogU:771737926936559656> you guessed the winning number! (" + str(winningNum) + ")\nYou win 3 bread boxes!"

            #add 3 boxes as reward for guessing right
            fileBreadBoxR = open(userBreadBoxPath, "r")
            userBoxes = int(fileBreadBoxR.readline())
            fileBreadBoxR.close()

            userBoxes += 3

            fileBreadBoxW = open(userBreadBoxPath, "w")
            fileBreadBoxW.write(str(userBoxes))
            fileBreadBoxW.close()

            #deactivate the game
            guessStatusPath = os.path.join("User levels/", user + " guess game status.txt")
            gameDeactivate = open(guessStatusPath, "w")
            gameDeactivate.write("false")
            gameDeactivate.close()

            #save the time finished so i can check cooldown
            currTime = getTime()
            completeName = os.path.join("User levels/", user + " guess game cooldown.txt")
            file = open(completeName, "w")
            file.write(str(currTime)) #send the current time because it is now the previous time
            file.close()
        else:
            availGuesses = getAvailableGuesses(user)
            availGuesses -= 1
            output = "<:Weird:568458482840502302> not the right number (" + str(availGuesses) + " guesses remaining)"
            if (availGuesses <= 0):
                output += "\nYou are out of guesses! The number was " + str(winningNum) + ". You can start another game in 10 minutes"

                guessStatusPath = os.path.join("User levels/", user + " guess game status.txt")
                gameDeactivate = open(guessStatusPath, "w")
                gameDeactivate.write("false")
                gameDeactivate.close()

                #save the time finished so i can check cooldown
                currTime = getTime()
                completeName = os.path.join("User levels/", user + " guess game cooldown.txt")
                file = open(completeName, "w")
                file.write(str(currTime)) #send the current time because it is now the previous time
                file.close()
        

        availGuesses = getAvailableGuesses(user)
        availGuesses -= 1
        
        

        availableGuessPath = os.path.join("User levels/", user + " guess game available guesses.txt")
        availGuessFileW = open(availableGuessPath, "w")
        availGuessFileW.write(str(availGuesses))
        availGuessFileW.close()
                
    return output
        

    




@bot.command()
async def lobby(ctx, *, a: custTimer):
    #await ctx.send("Lobby ping in " + a)
    await ctx.send(a)



@bot.event
async def on_message(message):  # event that happens per any message.
        
    print(f"{message.channel}: {message.author}: {message.author.name}: {message.content}")

    #reset cooldowns for all users (only for my account)
    if str(message.author) == "hoody#9652" and "!!resetcooldown" in message.content.lower():
        resetTime()

    #schedule a time for the bot to ping Among us role in x hours
    if str(message.author) == "hoody#9652" and "start lobby" in message.content.lower():
        msg = message.content.split()
        if (int(msg[2]) == 1):
            await message.channel.send('lobby starts in ' + msg[2] + ' hour')
            await message.channel.send("<@&747923936829898952> " + custTimer(msg[2]))
        else:
            await message.channel.send('lobby starts in ' + msg[2] + ' hours')
            await message.channel.send("<@&747923936829898952> " + custTimer(msg[2]))


    #BAKE
    if  str(message.author) != "The Baker#0723" and str(message.channel) == "bakery" and str(message.content) != "!bakecount" and "bake" in message.content.lower():
        if (checkTime(message.author)):
            await message.channel.send(testRand(str(message.author)))
        else:
            await message.channel.send("you already baked :)")

    #check points
    if str(message.author) != "The Baker#0723" and str(message.channel) == "bakery" and "!bread" in message.content.lower():
        msg = message.content.split()
        try:
            user = msg[1]
            await message.channel.send(checkLevel(checkName(user)))
        except:
            await message.channel.send(checkLevel(str(message.author)))

    #check test count
    if str(message.channel) == "bakery" and "!bakecount" in message.content.lower():
        await message.channel.send(checkTestCount())

    #gamble EZ
    if  str(message.channel) == "bakery" and "!gamble" in message.content.lower():
        msg = message.content.split()
        #if (checkGambleTime(message.author.name)):
        await message.channel.send(gamble(str(message.author), msg[1]))
        #else:
        #await message.channel.send("you already gambled :)")

    #check leaderboard
    if str(message.channel) == "bakery" and str(message.content) == "!lb":
        await message.channel.send(leaderboard())

    #check gamble count
    if str(message.channel) == "bakery" and str(message.content) == "!gcount":
        await message.channel.send(checkGambleCount())


    #donate bread to another user
    if str(message.channel) == "bakery" and "!give" in message.content.lower():
            msg = message.content.split()
            if (len(msg) > 3): #check if there's more than 3 elements in the message, if so, then the username being given most likely has a space
                try:
                    spaced_msg = message.content.split("\n") #users enter the bread on a new line when the username has a space, so split on newline
                except:
                    print("could not split with newline")
                bread = spaced_msg[1] #everything after the newline is the bread amount
                user = spaced_msg[0][6:] #before the newline is the username, but splice out the part that says "!give " to get only the username
            else:
                user = msg[1]
                bread = msg[2]
                
            await message.channel.send(giveBread(str(message.author), user, bread))


    


    #useless function that responds when a user @'s it
    if str(message.channel) == "bakery" and "<@!416447447515267072>" in message.content:
        await message.channel.send("dont @ me")

    #useless function to output the insertion sort algorithm cuz i didnt know how to copy from raspi to my pc
    if str(message.channel) == "bakery" and "!code" in message.content.lower():
        message1 = "```python\n"
        message1 += "for i in range(0, len(userList)):\n\tj = i\n\twhile (j > 0 and pointsList[j] < pointsList[j - 1]): #if the number before the current number is lower, true"
        message1 += "\n\t\ttemp = pointsList[j]\n\t\ttempName = userList[j]\n\t\t#swap numeric values\n\t\tpointsList[j] = pointsList[j - 1]"
        message1 += "\n\t\tpointsList[j - 1] = temp\n\t\t#swap names so that the indicies of each list (name and points) match"
        message1 += "\n\t\tuserList[j] = userList[j - 1]\n\t\tuserList[j - 1] = tempName\n\t\tj -= 1\n\ti += 1"
        message1 += "```"
        await message.channel.send(message1)
        
    #useless function that reminds people test has changed to bake
    if str(message.channel) == "bakery" and str(message.content.lower()) == "test":
        await message.channel.send("test has changed to bake")


    

                # STORE COMMANDS
    #open the store 
    if str(message.channel) == "bakery" and str(message.content.lower()) == "!store":
        await message.channel.send(store(str(message.author)))

    #buy an item
    if str(message.channel) == "bakery" and "!buy" in message.content.lower():
        msg = message.content.split()
        await message.channel.send(storePurchase(str(message.author), msg[1]))




                # BREAD BOX COMMANDS
                
    #open a bread box 
    if str(message.channel) == "bakery" and str(message.content.lower()) == "!open":
        await message.channel.send(openBreadBox(str(message.author)))

    #check how many boxes you have
    if str(message.channel) == "bakery" and str(message.content.lower()) == "!boxes":
        await message.channel.send(getBreadBoxCount(str(message.author)))

    #check how many boxes you have left to buy today (15 max)
    if str(message.channel) == "bakery" and str(message.content.lower()) == "!boxlimit":
        await message.channel.send(getBoxPurchases(str(message.author)))
    
    #useless function to remind people that points was changed to bread
    if str(message.author) != "The Baker#0723" and str(message.channel) == "bakery" and "!points" in message.content.lower():
        await message.channel.send("!points was changed to !bread")

    #give a user a bread box    
    if str(message.channel) == "bakery" and "!trade" in message.content:
        msg = message.content.split()
        user = msg[1]
        try:
            amount = msg[2]
        except:
            await message.channel.send("Enter an amount to trade (e.g.: !trade The Baker 2)")
            
        if (int(msg[2]) > 0):
            await message.channel.send(tradeBox(str(message.author), user, amount))
        else:
            amount = 1
            await message.channel.send(tradeBox(str(message.author), user, amount))




                # LOTTERY COMMANDS
                
    #allow predictions to start
    if str(message.author) == "hoody#9652" and str(message.channel) == "bakery" and str(message.content.lower()) == "!start predictions":
        await message.channel.send(lotteryPredictions())

    #command for submitting a guess
    if str(message.channel) == "bakery" and "!ticket" in message.content.lower():
        msg = message.content.split()
        try: 
            userGuess = msg[1]
        except:
            await message.channel.send("enter a number to guess (between 1 and 200)")                       
        await message.channel.send(userPredict(str(message.author), userGuess))

    #starts the lottery and checks if there's a winner
    if str(message.author) == "hoody#9652" and str(message.channel) == "bakery" and str(message.content.lower()) == "!start lottery":
        await message.channel.send("<:pausechamp:793988297637625958>")
        for i in range(0, 3):
            await message.channel.send("...\n")
            time.sleep(2)
        await message.channel.send(startLottery())

    #stops predictions from being allowed
    if str(message.author) == "hoody#9652" and str(message.channel) == "bakery" and str(message.content.lower()) == "!end lottery":
        await message.channel.send(stopLottery())

    #check prizepool
    if str(message.channel) == "bakery" and "!prize" in message.content.lower():
        await message.channel.send(checkJackpot())

    #donate to the jackpot
    if str(message.channel) == "bakery" and "!add" in message.content.lower():
        msg = message.content.split()
        try:
            donation = msg[1]
        except:
            await message.channel.send("enter a percentage to donate (e.g.: \"!add 1\" donates 1% of your bread)")
                                       
        await message.channel.send(donateToJackpot(str(message.author), donation))

    #return how many guesses a user has available in the lottery
    if str(message.channel) == "bakery" and str(message.content) == "!guesscount":
        await message.channel.send(getGuessCount(str(message.author)))

    if str(message.channel) == "bakery" and str(message.content) == "ticket list":
        await message.channel.send(checkTickets())




                # GUESSING GAME COMMANDS
                
    #start the guess game
    if str(message.channel) == "bakery" and str(message.content).lower() == "start guessing":
        await message.channel.send(startGuessGame(str(message.author)))

    #read a user's guess
    if str(message.channel) == "bakery":
        gameStatusPath = os.path.join("User levels/", str(message.author) + " guess game status.txt")
        if (checkIfGuessGameActive(gameStatusPath) == "true"):
            try:
                number = int(message.content)
            except:
                print("failed to parse messange.content into int")
            #try:    
            await message.channel.send(readGuess(str(message.author), number))
            #except:
            #print("not a guess")


    if str(message.channel) == "bakery" and str(message.content) == "tesst":
        gameStatusPath = os.path.join("User levels/", str(message.author) + ".txt")
        availGuessFile = open(gameStatusPath, "r")
        availGuesses = int(availGuessFile.readline())
        availGuessFile.close()
        await message.channel.send(str(availGuesses))

    if str(message.author) == "hoody#9652" and str(message.channel) == "bakery" and str(message.content.lower()) == "image":
        #with open('test.jpeg', 'rb') as f:
        #picture = discord.File(f)
        await message.channel.send(file=discord.File('test.jpeg'))

        
bot.run('NDE2NDQ3NDQ3NTE1MjY3MDcy.Wo-U6A.KWlyZW1lxDnPoIo-DDriLUouwSI')



#      roles
# <@&747923936829898952> @among us (ping) role

#      emojis
# <:EZ:406827146632232972> 
# <:OMEGALUL:420884833288454163> 
# <:monkaS:384078011366113280>
# <:squadw:771036304874930178>
# <:KermitTea:303786824831336448>
# <:pepelaugh:771033359837036564>
# <:FeelsBadMan:303787556213096458>
# <:MEGALUL:761218566132334622>
# <:angry_pepe:406826858139746313>
# <:Weird:568458482840502302>
# <:emoji_27:608818423430119454> Pepe holding knife
# <:Sadge:761225325723123732>
# <:PogChamp:304416481528250369>
# <:FeelsAmazingMan:400752334856126465>
# <:5Head:771067313738481674>
# <:stonks:761227625423044629>
# <:PogU:771737926936559656>
# <:FeelsGoodMan:452068213665300490>
# <:peepofat:775341285544427561>
# <:WeirdChamp:778827632053583872>
# <:pausechamp:793988297637625958>
