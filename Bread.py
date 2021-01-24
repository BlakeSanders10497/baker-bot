import os
import asyncio
import random
import discord
import asyncio
import random
import time
from datetime import datetime

import DatabaseOperations
import Utilities


roke = "<:Sadge:761225325723123732> you broke it (-1 points)"
notWorking = "<:pepelaugh:771033359837036564> not working (0 points)"
halfWorking = "<:ThinkingDank:385065840418095115> half working (1 point)"
working = "<:PogU:771737926936559656> working (2 points)"
reallyWorking = "<:FeelsAmazingMan:400752334856126465> really working (4 points)"
fixed = "<:5Head:771067313738481674> improved it (7 points)"
stonks = "<:stonks:761227625423044629> STONKS (50 points)"

ovenbroke = "<:Sadge:761225325723123732> oven not working"
undercooked = "<:pepelaugh:771033359837036564> undercooked"
nobutter = "<:ThinkingDank:385065840418095115> not enough butter"
nopowder = "<:ThinkingDank:385065840418095115> needs more baking powder"
cooked = "<:PogU:771737926936559656> cooked nicely"
crisp = "<:peepofat:775341285544427561> crisp bread"
perfect = "<:FeelsAmazingMan:400752334856126465> cooked to perfection"
gordon = "<:stonks:761227625423044629> gordon ramsey of baking"


responses = [ovenbroke, 
             undercooked, undercooked,
             nobutter, nobutter,
             nopowder, nopowder,
             cooked, cooked,
             crisp, crisp, crisp,
             perfect, perfect]


#after saying bake in chat, the function picks a random response from the list above and awards the user those points
def bake(user):
    userData = DatabaseOperations.getDataList(user)

    name = userData['name'] 
    points = int(userData['bread'])
    butterLife = int(userData['butter life'])

    if (int(points) < 1000): #if users points are below 10000, stick to normal point giving system, if not, then it uses percentages 
        num = random.randrange(0, len(responses)) #random number between 0 and # of responses
        if (butterLife < 20 and butterLife > 0):
            reward = num + random.randrange(5, 15)
            userData['butter life'] = str(butterLife + 1)
        else:
            reward = num
        status = responses[num] + " (" + str(reward) + " bread)"
    else:
        if (butterLife < 20 and butterLife > 0):
            num = random.randrange(3, 13)
            userData['butter life'] = str(butterLife + 1)
        else:
            num = random.randrange(1, 10)

        percent = num / 1000 #get a number between 0.001 and 0.01    
        luckyNumber = random.randrange(1, 40)
        
        if (luckyNumber == 20):
            percent = 0.25
            reward = int(points) * percent #Special reward that gives 25% if the lucky number is 20
            text = "<:stonks:761227625423044629> gordon ramsey of baking"
        else:
            reward = int(points) * percent #get the percent of the user's points
            text = responses[num]
            
        status = text + " (+{:,} bread, ".format(int(reward)) + "{:.2f}".format(percent * 100) + "%)"
    
    bakes = int(userData['daily bakes']) + 1
    
    #increase daily and total bakes
    userData['daily bakes'] = str(bakes)
    userData['bakes'] = str(int(userData['bakes']) + 1)

    #give user a bread box for every 10 bakes
    if (bakes % 10 == 0):
        userData['bread box'] = str(int(userData['bread box']) + 1)
        status += "\nyou received 1 bread box for reaching " + str(bakes) + " bakes!"
        
        
    #check butter status
    if (butterLife >= 20):
        userData['butter life'] = '0'
        status += "\nthe butter has expired"
    
    userData['bread'] = str(int(points) + int(reward)) + "\n" #update user's points
    
    
    #write to database
    DatabaseOperations.writeToDB(userData)
    
    
    
    #save to total bakes (all users combined)
    bakeCountPath = os.path.join("Stats/", "bake-count.txt")
    file = open(bakeCountPath, "r")
    count = int(file.readline())
    count += 1 
    file.close()
    file = open(bakeCountPath, "w")
    file.write(str(count))
    file.close()
    
    
    return status



#a user enters the amount they want to gamble, and the function randomly choses a number in the resultList and multiplies the 
#  amount the bet by that number and adds it to the user's total points. e.g.: if number chosen is -1, points (5) * -1 = -5,
#    points (5) + -5 = 0
async def gamble(user):
    msg = user.content.split()
    try:
        amount = int("".join(msg[1].split(",")))
    except:
        await user.channel.send("Invalid bread amount")
    
    userData = DatabaseOperations.getDataList(user) #get a dictionary of user's data
    resultList = [-1, -1, -1, -1, 0, 1, 1, 1, 1] 
    
    bread = int(userData['bread'])
    
    if (bread <= 0): #cant gamble if at or below 0 bread
        response = "you're too broke to gamble <:Sadge:761225325723123732>"
    elif (amount > bread): 
        response = "you can't gamble more than you have <:Weird:568458482840502302>"
    else:
        num = int(random.randrange(0,8))
        value = amount * resultList[num]
        bread += value
  
        userData['bread'] = str(bread) + "\n"
        DatabaseOperations.writeToDB(userData)
        
        if (num <= 3):
            response = "You lost {:,} bread".format(value)
        elif (num == 4):
            response = "You didn't gain or lose any bread"
        elif (num >= 5):
            response = "You gained {:,} bread".format(value)


        #update gamble count
        completeName = os.path.join("Stats/", "gamble-count.txt")
        file2 = open(completeName, "r")
        count = int(file2.readline()) #extract gamble count value
        count += 1 #increase it
        file2.close()
        file2 = open(completeName, "w")
        file2.write(str(count)) #send new gamble count back in
        file2.close()
        
    await user.channel.send(response)





#check how many points a user has
async def checkLevel(user):
    found = False
    msg = user.content.split()
    if (len(msg) > 1):
        username = " ".join(msg[1:])
        userData, found = DatabaseOperations.searchUser(username)
        if (not found):
            await user.channel.send("could not find user named: " + username)
    else:
        userData = DatabaseOperations.getDataList(user)
        
    if (userData['nickname'] == ""):
        name = userData['name']
    else:
        name = userData['nickname']
        
    points = int(userData['bread'])
    
    await user.channel.send(f"{name}'s bread: {points:,}")


  


#takes X bread from the author and gives specified user X bread 
async def giveBread(user):
    response = ""
    msg = user.content.split()
    try:          
        donateeName = " ".join(msg[2:]) #get donatee's name from the author's message
    except:
        await user.channel.send("invalid user name")
    try:
        breadAmount = int("".join(msg[1].split(",")))
    except:
        await user.channel.send("Invalid bread amount")
            
            
    userData = DatabaseOperations.getDataList(user) #get the donator's data in dictionary form
    donateeData = DatabaseOperations.searchUserByNickname(donateeName) #search for a user in the database with given input

    if (len(donateeData) == 0): #if user is not found with matching nickname
        donateeData = DatabaseOperations.searchUserByUsername(donateeName) #search by username instead (includes tag - e.g.: #1111)

    if (len(donateeData) == 0): #if still not found
        response = "```Error: no user found with nickname " + donateeName + "\nIf user has not set their nickname, include their tag```"
    else:
        donatorBread = int(userData['bread'])
        if (breadAmount <= donatorBread and breadAmount >= 0):
            #get points of the person being given bread
            donateeData['bread'] = str(int(donateeData['bread']) + breadAmount) + "\n"

            #subtract points from donator's total
            userData['bread'] = str(donatorBread - breadAmount) + "\n"

            DatabaseOperations.writeToDB(userData)
            DatabaseOperations.writeToDB(donateeData)
            
            response = "donated {:,} bread to {} :)".format(breadAmount, donateeName)
        else:
            response = "you can't donate more bread than you have <:Weird:568458482840502302>"

    
    await user.channel.send(response)
    
    
