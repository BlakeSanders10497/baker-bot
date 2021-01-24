import discord
import DatabaseOperations
import BreadBox
import random

def maxBreadBoxPurchases(user):
    reachedLimit = False
    userData = DatabaseOperations.getDataList(user)

    if (int(userData['bread box purchases']) >= 5):
        reachedLimit = True

    return reachedLimit



#returns the amount of purchases of bread boxes allowed today for the user
def getBoxPurchases(user):
    userData = DatabaseOperations.getDataList(user)
    
    return "You have " + str((int(userData['bread box purchases']) - 5) * -1) + " boxes left to buy today"



def openBreadBox(user):
    userData = DatabaseOperations.getDataList(user)
    
    msg = user.content.split()
    try:
        if (msg[1] == "all"):
            boxes = int(userData['bread box'])
        else:
            boxes = int(msg[1])
    except:
        boxes = 1
        
    
    output = ""
    
    if (int(userData['bread box']) < boxes):
        output = "you dont have any bread boxes to open"
    else:
        totalReward = 0
        totalPercent = 0
        percent = 0
        for i in range(0, boxes):
            if (int(userData['bread']) > 1000):
                percent = random.randrange(1, 5) / 100
                reward = int(int(userData['bread']) * percent)
                totalPercent += percent
            else:
                reward = int(random.randrange(10, 30))
            userData['bread'] = str(int(userData['bread']) + int(reward)) + "\n"
                
            
            totalReward += reward


        userData['bread box'] = str(int(userData['bread box']) - boxes) 
        
        DatabaseOperations.writeToDB(userData)
        
        if (boxes > 1):
            output = "{} bread boxes gave you {:,}".format(boxes, int(totalReward)) + " bread <:PogU:771737926936559656>"
            if (percent > 0):
                output += " (net gain: {:.2f}".format(totalPercent * 100) + "%)"

        elif (percent > 0):
            if (percent <= 0.02 and percent > 0):
                output = "Bread box gave you {:,}".format(int(reward)) + " bread <:FeelsBadMan:303787556213096458>" + " ({:.2f}".format(percent * 100) + "%)"
            elif (percent > 0.02 and percent <= 0.05):
                output = "Bread box gave you {:,}".format(int(reward)) + " bread <:FeelsGoodMan:452068213665300490>" + " ({:.2f}".format(percent * 100) + "%)"
            elif (percent > 0.05):
                output = "Bread box gave you {:,}".format(int(reward)) + " bread <:PogU:771737926936559656>" + " ({:.2f}".format(percent * 100) + "%)"
        else:
            if (reward <= 16):
                output = "Bread box gave you {:,}".format(int(reward)) + " bread <:FeelsBadMan:303787556213096458>"
            elif (reward > 16 and reward <= 22):
                output = "Bread box gave you {:,}".format(int(reward)) + " bread <:FeelsGoodMan:452068213665300490>"
            elif (reward > 23):
                output = "Bread box gave you {:,}".format(int(reward)) + " bread <:PogU:771737926936559656>"
        
    return output
    



async def tradeBox(user):
    msg = user.content.split()
    
    try:
        donateeName = " ".join(msg[2:])
        amount = msg[1]
    except:
        await user.channel.send("```Error\n\nCorrect syntax: !trade 3 The Baker")
    
    
    userData = DatabaseOperations.getDataList(user) #get the donator's data in dictionary form
    
    donateeData = DatabaseOperations.searchUserByNickname(donateeName) #search for a user in the database with given input
    print(donateeData)
    response = ""
    
    if (len(donateeData) == 0): #if user is not found with matching nickname
        donateeData = DatabaseOperations.searchUserByUsername(donateeName) #search by username instead (includes tag - e.g.: #1111)

    if (len(donateeData) == 0): #if still not found
        response = "```Error: no user found with nickname " + donateeName + "\nIf user has not set their nickname, include their tag```"
    else:
        donatorBoxes = int(userData['bread box'])
        if (int(amount) > donatorBoxes):
            response = "you cant donate more than you have <:Weird:568458482840502302>"
        else:
            userData['bread box'] = str(donatorBoxes - int(amount)) #subtract from donator's bread boxes
            donateeData['bread box'] = str(int(donateeData['bread box']) + int(amount)) #add to donatee's bread boxes

            DatabaseOperations.writeToDB(userData)
            DatabaseOperations.writeToDB(donateeData)
            
            response = "donated " + str(amount) + " bread boxes to " + donateeName + " :)"

    await user.channel.send(response)



def getBreadBoxCount(user):
    userData = DatabaseOperations.getDataList(user)
    
    output = ""
    
    userBoxes = int(userData['bread box'])

    if (userBoxes == 0):
        output = "You have no bread boxes"
    if (userBoxes == 1):
        output = "You have " + str(userBoxes) + " bread box"
    if (userBoxes > 1):
        output = "You have " + str(userBoxes) + " bread boxes"


    return output
