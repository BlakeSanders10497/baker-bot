import discord
import DatabaseOperations
import BreadBox
import Utilities
import random
import asyncio

def maxBreadBoxPurchases(user):
    reachedLimit = False
    userData = DatabaseOperations.getDataList(user)

    if (userData['bread box purchases'] >= 5):
        reachedLimit = True

    return reachedLimit



#returns the amount of purchases of bread boxes allowed today for the user
def getBoxPurchases(user):
    userData = DatabaseOperations.getDataList(user)
    
    return "You have " + str((int(userData['bread box purchases']) - 5) * -1) + " boxes left to buy today"



async def openBreadBox(user):
    userData = DatabaseOperations.getDataList(user)
    
    msg = user.content.split()
    try:
        if (msg[1] == "all"):
            boxes = userData['bread box']
        else:
            boxes = int(msg[1])
    except:
        boxes = 1
        
    
    output = ""
    
    if (userData['bread box'] < boxes or userData['bread box'] == 0):
        output = "you dont have that many boxes :("
    else:
        totalReward = 0
        totalPercent = 0
        percent = 0
        for i in range(0, boxes):
            if (userData['bread'] > 1000):
                percent = random.randrange(1, 5) / 100
                reward = int(userData['bread'] * percent)
                totalPercent += percent
            else:
                reward = random.randrange(10, 30)
            userData['bread'] = userData['bread'] + reward
                
            
            totalReward += reward


        userData['bread box'] = userData['bread box'] - boxes 
        
        DatabaseOperations.writeToDB(userData)
        
        if (boxes > 1):
            output = "{} bread boxes gave you {:,}".format(boxes, int(totalReward)) + " bread :star_struck:"
            if (percent > 0):
                output += " (net gain: {:.2f}".format(totalPercent * 100) + "%)"

        elif (percent > 0):
            if (percent <= 0.02 and percent > 0):
                output = "Bread box gave you {:,}".format(reward) + " bread :pensive:" + " ({:.2f}".format(percent * 100) + "%)"
            elif (percent > 0.02 and percent <= 0.05):
                output = "Bread box gave you {:,}".format(reward) + " bread :grimacing:" + " ({:.2f}".format(percent * 100) + "%)"
            elif (percent > 0.05):
                output = "Bread box gave you {:,}".format(reward) + " bread :sunglasses:" + " ({:.2f}".format(percent * 100) + "%)"
        else:
            if (reward <= 16):
                output = "Bread box gave you {:,}".format(reward) + " bread :pensive:"
            elif (reward > 16 and reward <= 22):
                output = "Bread box gave you {:,}".format(reward) + " bread :grimacing:"
            elif (reward > 23):
                output = "Bread box gave you {:,}".format(reward) + " bread :sunglasses:"
    
    embed = await Utilities.getEmbedMsg(body_text = output)
    await user.channel.send(embed = embed)
    



async def tradeBox(user, bot):
    msg = user.content.split()
    
    try:
        donateeName = " ".join(msg[2:])
        amount = int(msg[1])
        if (donateeName == ""):
            msg = msg + amount
    except:
        error_msg = await user.channel.send("```css\n[Invalid command]\nCorrect syntax: !trade 3 The Baker```")
        return
    
    found = False
    body_text = ""
    userData = DatabaseOperations.getDataList(user) #get the donator's data in dictionary form
    donateeData, found = DatabaseOperations.searchUser(donateeName) #search for a user in the database with given input
    
    
    if (not found): #if user is not found with matching nickname
        donateeData, found = DatabaseOperations.looseSearch(donateeName) #use find() to check if the name is somewhere in the database
        if found:
            found, donateeName, donateeData, body_text, error_msg = await Utilities.displayUserRecommendation(found, donateeName, donateeData, user, bot)

    try:
        if (found and userData['id'] == donateeData['id']): #compare id of author and user they are donating to
            body_text = ":face_with_raised_eyebrow: you cant trade to yourself"
            found = False
    except:
        pass
    
    if (found): #if there was a match in any of the searches
        donatorBoxes = userData['bread box']
        if (amount > donatorBoxes): #make sure author isnt donating nore than they have
            body_text = ":face_with_raised_eyebrow: you cant trade more than you have"
        elif (amount <= 0): #make sure the amount of bread boxes being donated is more than 0
            body_text = ":face_with_raised_eyebrow: you cant trade less than 1 box"
        else:
            userData['bread box'] = donatorBoxes - amount #subtract from donator's bread boxes
            donateeData['bread box'] = donateeData['bread box'] + amount #add to donatee's bread boxes

            DatabaseOperations.writeToDB(userData) #save to database
            DatabaseOperations.writeToDB(donateeData) #save to database
            
            if (amount == 1):
                body_text = f"```fix\ntraded {amount} bread box to {donateeName} :)```"
            else:
                body_text = f"```fix\ndonated {amount} bread boxes to {donateeName} :)```"
    elif (body_text == ""):
        body_text = "```css\n[No user found]```"
    
    
    response = await Utilities.getEmbedMsg(body_text = body_text) #create an embed message
        
    try: # try to edit the message, but if it doesnt work, then it means no error message was sent, so send a new message
        await error_msg.clear_reactions()
        await error_msg.edit(embed = response)
    except:
        await user.channel.send(embed = response)



def getBreadBoxCount(user):
    userData = DatabaseOperations.getDataList(user)
    
    output = ""
    
    userBoxes = userData['bread box']

    if (userBoxes == 0):
        output = "You have no bread boxes"
    if (userBoxes == 1):
        output = "You have " + str(userBoxes) + " bread box"
    if (userBoxes > 1):
        output = "You have " + str(userBoxes) + " bread boxes"


    return output
