import os
import asyncio
import random
import discord
import asyncio
import random
import time
import logging
from datetime import datetime

import DatabaseOperations
import Utilities



ovenbroke = ":anger: oven not working"
undercooked = ":expressionless: undercooked"
nobutter = ":butter: not enough butter"
nopowder = ":face_with_monocle: needs more baking powder"
cooked = ":smiley: cooked nicely"
crisp = ":yum: crisp bread"
perfect = ":star_struck: cooked to perfection"
gordon = ":cook: gordon ramsey of baking"


responses = [ovenbroke, 
             undercooked, undercooked,
             nobutter, nobutter,
             nopowder, nopowder,
             cooked, cooked,
             crisp, crisp, crisp,
             perfect, perfect]


#after saying bake in chat, the function picks a random response from the list above and awards the user those points
async def bake(user):
    userData = DatabaseOperations.getDataList(user)

    name = userData['name'] 
    points = userData['bread']
    butterLife = userData['butter life']

    if (points < 1000): #if users points are below 10000, stick to normal point giving system, if not, then it uses percentages 
        num = random.randrange(0, len(responses)) #random number between 0 and # of responses
        if (butterLife < 20 and butterLife > 0):
            reward = num + random.randrange(5, 15)
            userData['butter life'] += 1
        else:
            reward = num
        status = responses[num] + " (" + str(reward) + " bread)"
    else:
        if (butterLife < 20 and butterLife > 0):
            num = random.randrange(3, 13)
            userData['butter life'] += 1
        else:
            num = random.randrange(1, 10)

        percent = num / 1000 #get a number between 0.001 and 0.01    
        luckyNumber = random.randrange(1, 40)
        
        if (luckyNumber == 20):
            percent = 0.25
            reward = int(points * percent) #Special reward that gives 25% if the lucky number is 20
            text = ":cook: gordon ramsey of baking"
        else:
            reward = int(points * percent) #get the percent of the user's points
            text = responses[num]
            
        status = text + " (+{:,} bread, ".format(reward) + "{:.2f}".format(percent * 100) + "%)"
    
    bakes = userData['daily bakes'] + 1
    
    #increase daily and total bakes
    userData['daily bakes'] += 1
    userData['bakes'] += 1

    #give user a bread box for every 10 bakes
    if (bakes % 10 == 0 and bakes != 0):
        userData['bread box'] += 1
        status += "\nyou received 1 bread box for reaching " + str(bakes) + " bakes!"
        
        
    #check butter status
    if (butterLife >= 20):
        userData['butter life'] = 0
        status += "\nthe butter has expired"
    
    userData['bread'] = points + reward #update user's points
    
    
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
    
    embed = await Utilities.getEmbedMsg(body_text = status)
    await user.channel.send(embed = embed)
    



#a user enters the amount they want to gamble, and the function randomly choses a number in the resultList and multiplies the 
#  amount the bet by that number and adds it to the user's total points. e.g.: if number chosen is -1, points (5) * -1 = -5,
#    points (5) + -5 = 0
async def gamble(user):
    msg = user.content.split()
    try:
        amount = int("".join(msg[1].split(",")))
    except:
        embed = await Utilities.getEmbedMsg(body_text = "```css\nInvalid bread amount```")
        await user.channel.send(embed = embed)
    else:
        userData = DatabaseOperations.getDataList(user) #get a dictionary of user's data
        resultList = [-1, -1, -1, -1, 0, 1, 1, 1, 1] 
        
        bread = userData['bread']
        
        if (bread <= 0): #cant gamble if at or below 0 bread
            response = "you're too broke to gamble :dissapointed:"
        elif (amount > bread): 
            response = "you can't gamble more than you have :face_with_raised_eyebrow:"
        elif (amount < 1):
            response = "you can't gamble less than 1 bread :face_with_raised_eyebrow:"
        else:
            num = random.randrange(0,8)
            value = amount * resultList[num]
            bread += value
      
            userData['bread'] = bread
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
        
        embed = await Utilities.getEmbedMsg(body_text = response)
        await user.channel.send(embed = embed)





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
        
    points = userData['bread']
    
    await user.channel.send(f"{name}'s bread: {points:,}")


  


#takes X bread from the author and gives specified user X bread 
async def giveBread(user, bot):
    msg = user.content.split()
    
    try:
        donateeName = " ".join(msg[2:])
        amount = int(msg[1])
        
        if (donateeName == ""):
            msg = msg + amount
    except:
        error_msg = await user.channel.send("```css\n[Invalid command]\nCorrect syntax: !give 3 The Baker```")
        return
    
    body_text = ""
    found = False
    
    userData = DatabaseOperations.getDataList(user) #get the donator's data in dictionary form
    donateeData, found = DatabaseOperations.searchUser(donateeName) #search for a user in the database with given input
    
    
    if (not found): #if user is not found with matching nickname or username
        donateeData, found = DatabaseOperations.looseSearch(donateeName) #use find() to check if the name is somewhere in the database
        if (found):
            found, donateeName, donateeData, body_text, error_msg = await Utilities.displayUserRecommendation(found, donateeName, donateeData, user, bot)
    else:
        found = True
    try:
        if (found and userData['id'] == donateeData['id']): #compare id of author and user they are donating to
            body_text = ":face_with_raised_eyebrow: you cant give to yourself"
            found = False
    except:
        pass
    
    if (found): #if there was a match in any of the searches
        donatorBread = userData['bread']
        if (amount > donatorBread): #make sure author isnt donating nore than they have
            body_text = ":face_with_raised_eyebrow: you cant give more than you have"
        elif (amount <= 0): #make sure the amount of bread  being given is more than 0
            body_text = ":face_with_raised_eyebrow: you cant give less than 1 bread"
        else:
            userData['bread'] = donatorBread - amount #subtract from donator's bread 
            donateeData['bread'] = donateeData['bread'] + amount #add to donatee's bread 
            
            DatabaseOperations.writeToDB(userData) #save to database
            DatabaseOperations.writeToDB(donateeData) #save to database
            
            body_text = f"```fix\ngave {amount} bread to {donateeName} :)```"
    elif (body_text == ""):
        body_text = "```css\n[No user found]```"
        
    response = await Utilities.getEmbedMsg(body_text = body_text) #create an embed message
        
    try: # try to edit the message, but if it doesnt work, then it means no error message was sent, so send a new message
        await error_msg.clear_reactions()
        await error_msg.edit(embed = response)
    except:
        await user.channel.send(embed = response)
    
    
