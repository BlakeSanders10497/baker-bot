import discord
from discord.ext import commands
import asyncio
import random
import time
from datetime import datetime
import os.path

import Leaderboard #mine
import DriveFunctions #mine

from os import path

bot = commands.Bot(command_prefix='.', description='A bot that greets the user back.')


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


def getUserData(user, data):
    
    index = -1 #index will be -1 if no user is found in the database
    for i in range(0, len(data)):
        currName = (data[i].split(","))[0] #parse the name out of the lines of data
        print(currName)
        if (currName == user): #check if the user who baked is in the database
            index = i #this will be the row in User Database.txt that the user belongs to

    print(data)

    return index


def testRand(userName):

    #get file ID and download the file from google drive
    GDfile_ID = DriveFunctions.download('User Database.txt')

    with open('User Database.txt', 'r') as file: #read the database file
        data = file.readlines()
        
    index = getUserData(userName, data)

    if (index == -1):
        print("user not found in database")
        
    userData = data[index].split(',') #get the user's row from the database

    name = userData[0] #first column is name
    points = userData[1]
    boxes = userData[2]
    
    print(index)
    print(points)

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
        

    strUserData = name + "," + str((int(points) + int(reward))) + "," + boxes #put the data back into one string
    data[index] = strUserData #set their line in the database to the updated info

    print(data)

    
    with open('User Database.txt', 'w') as file: #write it to the local file
        file.writelines(data)
   
    filePath = "User Database.txt"
    
    DriveFunctions.upload_files(filePath) #upload to google
    
    
    
    return status



def deleteFile(filePath):
    os.remove(filePath) #delete the file locally
    return True





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







#check how many points a user has
def checkLevel(userName):
    completeName = os.path.join("User levels/", userName + ".txt")

    checkIfExists(completeName)
    
    file = open(completeName, "r")
    level = int(file.readline())
    #response = f"{level:,}"
    return f"{level:,} loaves of bread"





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
        




@bot.event
async def on_message(message):  # event that happens per any message.
        
    print(f"{message.channel}: {message.author}: {message.author.name}: {message.content}")

    #reset cooldowns for all users (only for my account)
    if str(message.author) == "hoody#9652" and "!!resetcooldown" in message.content.lower():
        resetTime()

    #BAKE
    if  str(message.author) != "The Baker#0723" and str(message.channel) == "bakery" and str(message.content) != "!bakecount" and "bake" in message.content.lower():
        await message.channel.send(testRand(str(message.author)))
        deleteFile('User Database.txt')
 

    #check points
    if str(message.author) != "The Baker#0723" and str(message.channel) == "baker" and "!bread" in message.content.lower():
        msg = message.content.split()
        try:
            user = msg[1]
            await message.channel.send(checkLevel(checkName(user)))
        except:
            await message.channel.send(checkLevel(str(message.author)))

 


    
    if str(message.channel) == "baker" and str(message.content.lower()) == "!gwins":
        await message.channel.send(file=discord.File(Leaderboard.leaderboard("Other files/", "guessing game user list.txt", " guess game wins.txt", "guessing game")))

    if  str(message.channel) == "baker" and str(message.content.lower()) == "test lb":
        await message.channel.send(file=discord.File(Leaderboard.leaderboard("User levels/", ",List of Account names.txt", ".txt", "bread")))


        
bot.run('TOKEN GOES HERE')


