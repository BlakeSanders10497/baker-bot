import discord
import DatabaseOperations
import BreadBox


def store(user):
    userData = DatabaseOperations.getDataList(user)
    output = ""
    
    if (int(userData['bread']) < 100):
        output = "you need at least 100 bread to shop at the store"
    else:
        breadBoxPrice = int(userData['bread']) * 0.02
        butterPrice = 100
        output = "```\t\t\tSTORE\n\n\tITEM\t\t\tPrice\n\n A1) Bread Box - ({:,}".format(int(breadBoxPrice)) + " bread)\n\n B2) Butter - ({:,}".format(butterPrice) + " bread)```"

    
    return output

        
    
async def storePurchase(user, item):
    userData = DatabaseOperations.getDataList(user)
    msg = user.content.split()
    output = ""

    try:
        amount = int(msg[2])
    except:
        #await user.channel.send("```Error\nCorrect syntax: !buy ID AMOUNT```")
        pass
    
    
    if (int(userData['bread']) < 50):
        output = "you need at least 100 bread to shop at the store"
    else:

        if (item == "A1"): #bread box 
            if (not BreadBox.maxBreadBoxPurchases(user)):
                price = int(userData['bread']) * 0.02
                userData['bread'] = str(int(userData['bread']) - int(price)) + "\n" #cost is 10% of user's bread
                userData['bread box'] = str(int(userData['bread box']) + 1) #add bread box to inventory
                userData['bread box purchases'] = str(int(userData['bread box purchases']) + 1) #add 1 to user box purchases of the day
    
                output = "Purchased 1 bread box (-{:,}".format(int(price)) + ")"
                
            else:
                output = "you have reached your bread box daily limit"

        elif (item == "B2"):
            if (int(userData['butter purchases']) < 1):
                price = 100
                userData['bread'] = str(int(userData['bread']) - int(price)) + "\n"
                userData['butter'] = str(int(userData['butter']) + 1)
                userData['butter purchases'] = str(int(userData['butter purchases']) + 1)

                output = "Purchased 1 stick of butter (-" + str(price) + ")"
            else:
                output = "you reached your daily butter limit"

        DatabaseOperations.writeToDB(userData)       
    await user.channel.send(output)
    
    
    
    
    
    
async def getButterCount(user):
    userData = DatabaseOperations.getDataList(user)

    output = ""
    
    userButter = int(userData['butter'])
    butterLife = int(userData['butter life'])
    butterLimit = 21
    if (userButter == 0):
        output = "You have no butter in your inventory"
    if (userButter >= 1):
        output = "You have " + str(userButter) + " butter in your inventory"

    if (butterLife > 0):
        output += "\nActive butter: " + str(butterLimit - butterLife) + " uses left"
    else:
        output += "\nno active butter"
        
    await user.channel.send(output)


async def useButter(user):
    userData = DatabaseOperations.getDataList(user)
    print(userData)
    if (int(userData['butter life']) > 0):
        response = "you already have butter active"
    else:
        userData['butter'] = str(int(userData['butter']) - 1)
        userData['butter life'] = '1'
        response = "butter is now active for 20 bakes!"
        DatabaseOperations.writeToDB(userData)
        
    await user.channel.send(response)
