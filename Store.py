import discord
import DatabaseOperations
import BreadBox
import Utilities

async def store(user):
    userData = DatabaseOperations.getDataList(user)
    output = ""
    
    if (userData['bread'] < 100):
        output = "you need at least 100 bread to shop at the store"
    else:
        breadBoxPrice = userData['bread'] * 0.02
        butterPrice = 100
        output = "```fix\n\t\t\tSTORE\n\n\tITEM\t\t\tPrice\n\n A1) Bread Box - ({:,}".format(int(breadBoxPrice)) + " bread)\n\n B2) Butter    - ({:,}".format(butterPrice) + " bread)```"

    embed = await Utilities.getEmbedMsg(body_text = output)
    await user.channel.send(embed = embed)

        
    
async def storePurchase(user, item):
    userData = DatabaseOperations.getDataList(user)
    msg = user.content.split()
    output = ""

    if (userData['bread'] < 50):
        output = "```fix\nyou need at least 50 bread to shop at the store```"
    else:

        if (item == "A1"): #bread box 
            if (not BreadBox.maxBreadBoxPurchases(user)):
                price = userData['bread'] * 0.02
                userData['bread'] = userData['bread'] - int(price) #cost is 2% of user's bread
                userData['bread box'] = userData['bread box'] + 1 #add bread box to inventory
                userData['bread box purchases'] = userData['bread box purchases'] + 1 #add 1 to user box purchases of the day
    
                output = "```fix\nPurchased 1 bread box (-{:,}".format(int(price)) + " bread)```"
                
            else:
                output = "```fix\nyou have reached your bread box daily limit```"

        elif (item == "B2"): #butter
            if (userData['butter purchases'] < 1):
                price = 100
                userData['bread'] = userData['bread'] - int(price)
                userData['butter'] = userData['butter'] + 1
                userData['butter purchases'] = userData['butter purchases'] + 1

                output = "```fix\nPurchased 1 stick of butter (-" + str(price) + " bread)```"
            else:
                output = "```fix\nyou reached your daily butter limit```"
        else:
            output = f"```fix\nCould not find item \"{item}\"```"
            
        DatabaseOperations.writeToDB(userData)
    
    embed = await Utilities.getEmbedMsg(body_text = output)
    await user.channel.send(embed = embed)
    
    
    
    
    
    
async def getButterCount(user):
    userData = DatabaseOperations.getDataList(user)

    output = ""
    
    userButter = userData['butter']
    butterLife = userData['butter life']
    butterLimit = 21
    if (userButter == 0):
        output = "You have no butter in your inventory"
    if (userButter >= 1):
        output = "You have " + str(userButter) + " butter in your inventory"

    if (butterLife > 0):
        output += "\nActive butter: " + str(butterLimit - butterLife) + " uses left"
    else:
        output += "\nno active butter"
    
    embed = await Utilities.getEmbedMsg(body_text = output)
    await user.channel.send(embed = embed)


async def useButter(user):
    userData = DatabaseOperations.getDataList(user)
    
    if (userData['butter life'] > 0):
        response = "you already have butter active"
    else:
        if (int(userData['butter']) > 0):
            userData['butter'] = userData['butter'] - 1
            userData['butter life'] = 1
            response = "butter is now active for 20 bakes!"
            DatabaseOperations.writeToDB(userData)
        else:
            response = "you dont have any butter"
    
    embed = await Utilities.getEmbedMsg(body_text = response)
    await user.channel.send(embed = embed)
