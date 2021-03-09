import time
from datetime import datetime
import random
import os.path
import asyncio
import DatabaseOperations
import discord
from os import path

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




def checkCooldown(user, cooldownType, cooldown): 
    """
    Compare previous time and current time and make sure it has been at least the amount of time it is passed
    
    param: user (discord Message object)
    param: cooldownType (string) - should match the name found in the database for the cooldown
    param: cooldown (int) - number of minutes
    
    return canBake (bool)
    return waitTime (string)
    """
    
    
    
    waitTime = ""
    canBake = checkDayMonthYear()
    if (canBake): #if new day, month, or year, reset cooldowns/limits for everyone
        resetTime()
    else:
        userData = DatabaseOperations.getDataList(user)
        prevTime = float(userData[cooldownType]) 
        currTime = getTime()
        if (currTime - float(prevTime) >= cooldown):
            canBake = True
        
            userData[cooldownType] = currTime #update timeout to current time
            DatabaseOperations.writeToDB(userData)
        else:
            canBake = False
        
        waitTime = str(cooldown - (float(currTime) - float(prevTime)))[:-2]
    
    
    return canBake, waitTime


#resets cooldowns and daily purchase limit because still havent fixed the damn time check function
def resetTime():
    data = DatabaseOperations.getDatabase()
    keys = list(data.keys())
    for id in keys:
        userData = data[id]
        userData['bread box purchases'] = 0
        userData['gg cooldown'] = -10   #guess game cooldown
        userData['timeout'] = -1 #bake cooldown
        userData['citygame cooldown'] = -15
        userData['flaggame cooldown'] = -10
        userData['butter purchases'] = 0
        userData['daily bakes'] = 0
        
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
    
    if (len(newName) > 20):
        response = "```css\nName must be fewer than 20 characters```"
    else:
        userData = DatabaseOperations.getDataList(user)
    
        oldName = userData['nickname']
        
        response = ""
        
        data = DatabaseOperations.getDatabase()
        keys = list(data.keys())
        for id in keys:
            if (data[id]['nickname'] == newName):
                response = "```css\nanother user already has that nickname\n```"
            
        if (response == ""): #no user with that nickname was found
            userData['nickname'] = newName
            DatabaseOperations.writeToDB(userData)
            if (oldName == ""):
                response = f"<@{userData['id']}> nickname changed to **{newName}**"
            else:
                response = f"<@{userData['id']}> nickname changed from **{oldName}** to **{newName}**"

    embed = await getEmbedMsg(body_text = response)
    await user.channel.send(embed = embed)



#returns the user's nickname if they have one
async def checkNickname(user):
    userData = DatabaseOperations.getDataList(user)

    if (userData['nickname'] == ""):
        response = "you have no set nickname, default is " + userData['name']
    else:
        response = "your nickname: " + userData['nickname']
    
    embed = await getEmbedMsg(body_text = response)
    await user.channel.send(embed = embed)
    

async def displayUserRecommendation(found, name, userData, user, bot):
    def check(reaction, userName):
        return userName == user.author
    
    if (found): #if there is a name containing donateeName, ask the user if that is user they are looking for
        title_text = "No user found"
        body_text = "```css\nDid you mean \"" + userData['name'] + "\"?```"
        error_msg = await user.channel.send(embed = await getEmbedMsg(title_text, body_text)) #create and send error message
        
        await error_msg.add_reaction("✅") # :white_check_mark:
        await error_msg.add_reaction("🚫") # :no_entry_sign:
        try:
            reaction, userName = await bot.wait_for('reaction_add', timeout = 15.0, check=check) #wait 15 seconds for a reaction (answer)
        except asyncio.TimeoutError:
            body_text = "request expired"
            found = False
        else:
            if (str(reaction) == "✅"):
                name = userData['nickname']
                if (len(name) == 0):
                    name = userData['name']
                found = True
            else:
                found = False
                body_text = "request cancelled"
    else:
        body_text = "```css\n[Error: no user found with nickname " + name + "]\nIf user has not set their nickname, include their tag```"
    
    return found, name, userData, body_text, error_msg


async def getEmbedMsg(title_text = "", body_text = "", message = "", userData = "", footer_text = ""):
    """
    Creates a simple embed message
    
    Parameters:
        title_text (str) : title text of the message
        body_text (str) : body text
        message (discord Message object) : used for adding the user's name and avatar to the message 
        userData (dict) : used to check if the user has a nickname, if so, use it in the message
    """
    embed = discord.Embed(title = title_text,
                            description = body_text,
                            color = 0xFFB500)
                        
    
    embed.set_footer(text = footer_text)
    if (message != "" and len(userData) != 0):
        if (userData['nickname'] == ""):
            display_name = str(message.author.name)
        else:
            display_name = userData['nickname']
        embed.set_author(name = display_name, icon_url = message.author.avatar_url)
    
    return embed




async def showProfile(message, bot):
    msg = message.content.split()
    
    try:
        input_name = " ".join(msg[1:])
    except:
        error_msg = await user.channel.send("```css\n[Invalid command]\nCorrect syntax: !profile or !profile [username or nickname]```")
        return
        
    user = False
    edit = False
    
    if (input_name == ""):
        userData = DatabaseOperations.getDataList(message)
        
        found = True
    else:
        userData, found = DatabaseOperations.searchUser(input_name)
        if (not found): 
            userData, found = DatabaseOperations.looseSearch(input_name)
            if found:
                found, name, userData, body_text, error_msg = await displayUserRecommendation(found, input_name, userData, message, bot)
                edit = True
    if found:
        user = await bot.fetch_user(userData['id'])
        title_text = f"{userData['name'][:-5]}'s Profile"
        body_text = f"\n**Bread**: {userData['bread']:,}\n------------------------------------------"
            
        new_embed = await getEmbedMsg(title_text, body_text)
        if userData['citygame played'] > 0:
            citygame_win_percentage = userData['citygame wins'] / userData['citygame played'] * 100
        else:
            citygame_win_percentage = 0.0
        
        if userData['flaggame played'] > 0:
            flaggame_win_percentage = userData['flaggame wins'] / userData['flaggame played'] * 100
        else:
            flaggame_win_percentage = 0.0
        
        if userData['gg played'] > 0:
            gg_win_percentage = userData['gg wins'] / userData['gg played'] * 100
        else:
            gg_win_percentage = 0.0
            
        
        new_embed.add_field(name = "Total bakes", value = userData['bakes'])
        new_embed.add_field(name = "Today's bakes", value = userData['daily bakes'])
        new_embed.add_field(name = "Bread boxes", value = userData['bread box'])
        new_embed.add_field(name = "Butter", value = userData['butter'])
        
        new_embed.add_field(name = "City Game wins", value = f"{userData['citygame wins']} ({citygame_win_percentage:.1f}%)")
        new_embed.add_field(name = "Flag Game wins", value = f"{userData['flaggame wins']} ({flaggame_win_percentage:.1f}%)")
        new_embed.add_field(name = "Guessing Game wins", value = f"{userData['gg wins']} ({gg_win_percentage:.1f}%)")
        
        if user and edit:
            new_embed.set_thumbnail(url = user.avatar_url)
            await error_msg.clear_reactions()
            await error_msg.edit(embed = new_embed)
        else:
            new_embed.set_thumbnail(url = user.avatar_url)
            await message.channel.send(embed = new_embed)
    else:
        body_text = "```css\n[No user found]```"
        new_embed = await getEmbedMsg(body_text = body_text)
        await message.channel.send(embed = new_embed)




async def helpMenu(bot, message, menu = "", previous_status = False):
    """
    Creates a help menu as an embed message
    
    Parameters:
        bot (discord Client object): used to wait_for() a reaction
        message (Message object): used for adding reactions, sending the message, getting user name and avatar
        menu (Message object): used to get the current menu message
        previous_status (bool): true when this function is called to return to the menu, false when it's the first call
    """
    message_id = message.id
    embed = discord.Embed(title = "Help",
                            description = "Categories",
                            color = 0xFFB500)
    embed.set_author(name = message.author, icon_url = message.author.avatar_url)
    embed.add_field(name = ":one: Games", value = "Flag game\nCity game\nGuessing game\nGambling")
    embed.add_field(name = ":two: Bread", value = "Bake\nStore\nBread box\nButter")
    embed.add_field(name = ":three: Other", value = "Profile\nNicknames\nLeaderboards\nSupport")
    
    if (previous_status == True):
        await menu.edit(embed=embed)
    else:
        menu = await message.channel.send(embed=embed)
        
    await menu.add_reaction("1️⃣") #1
    await menu.add_reaction("2️⃣") #2
    await menu.add_reaction("3️⃣") #3
    
    def check(reaction, userName):
        return userName == message.author
    
    
    reaction, userName = await bot.wait_for('reaction_add', check=check)
    if (str(reaction) == "1️⃣"):
        await menu.clear_reactions()
        await gameHelpMenu(bot, message, menu)
        await helpMenu(bot, message, menu, previous_status = True)
    elif (str(reaction) == "2️⃣"):
        await menu.clear_reactions()
        await breadHelpMenu(bot, message, menu)
        await helpMenu(bot, message, menu, previous_status = True)
    elif (str(reaction) == "3️⃣"):
        await menu.clear_reactions()
        await otherHelpMenu(bot, message, menu)
        await helpMenu(bot, message, menu, previous_status = True)


async def gameHelpMenu(bot, message, menu):
    """
    Edits the main menu message with the interface of the game menu
    """
    embed = discord.Embed(title = "Help",
                            description = "Games",
                            color = 0xFFB500)
    embed.set_author(name = message.author, icon_url = message.author.avatar_url)
    embed.set_footer(text = "click 1 to go back")
    
    embed.add_field(name = "Flag game", value = "__**!flaggame**__ to start\nAn image of a flag is displayed, and you must select the correct option\n*Reward: 1 bread box*")
    embed.add_field(name = "City game", value = "__**!citygame**__ to start\nAn image of city is displayed, and you must select the correct option\n*Reward: 1 bread box*")
    embed.add_field(name = "Guessing game", value = """__**start guessing**__ to start\nThe bot picks a number between 1 and 15, giving you 3 tries to guess it
                                                        \nSend a number to submit your guess\n*Reward: 3 bread boxes*""")
    embed.add_field(name = "Gambling", value = "__**!gamble [amount]**__\nChoose a number between 1 and the amount of bread you have, chances are 50/50 to win or lose")
    
    gameMenu = await menu.edit(embed = embed)
    await menu.add_reaction("1️⃣") #1
    previous_status = True
    def check(reaction, userName):
        return userName == message.author
    
    reaction, userName = await bot.wait_for('reaction_add', check=check)
    if (str(reaction) == "1️⃣"):
        await menu.clear_reactions()
        return


async def breadHelpMenu(bot, message, menu):
    embed = discord.Embed(title = "Help",
                            description = "Bread",
                            color = 0xFFB500)
    embed.set_author(name = message.author, icon_url = message.author.avatar_url)
    embed.set_footer(text = "click 1 to go back")
    
    embed.add_field(name = "Bake", value = """type __**bake**__ get between 0 and 14 bread if you have less than 1000 bread
                                              \nGives between 0.1 and 1.0% of your total bread if you have more than 1000 bread
                                              \nA bread box is received for every 10 bakes
                                              \n__**!give [amount] [username or nickname]**__ to give bread to another user""")
    embed.add_field(name = "Store", value = "__**!store**__ to show items\nLists items you can buy in the store\n__**!buy [item id]**__ to buy the item")
    embed.add_field(name = "Bread box", value = """__**!open**__ - gives you between 1-5% of your bread
                                                \n__**!open [amount]**__ to open multiple boxes
                                                \n__**!open all**__ to open all of your boxes
                                                \n__**!trade [amount] [username or nickname]**__ to trade to another user""")
    embed.add_field(name = "Butter", value = """Increases the odds of getting more bread from bakes.
                                                \nChances are between 5 and 15 if under 1000 bread, 0.3 to 1.3% if over.
                                                \n__**!butter**__ to show how much butter you have and if it is active\n
                                                __**!use butter**__ to use the butter""")
    
    gameMenu = await menu.edit(embed = embed)
    await menu.add_reaction("1️⃣") #1
    previous_status = True
    def check(reaction, userName):
        return userName == message.author
    
    reaction, userName = await bot.wait_for('reaction_add', check=check)
    if (str(reaction) == "1️⃣"):
        await menu.clear_reactions()
        return


async def otherHelpMenu(bot, message, menu):
    embed = discord.Embed(title = "Help",
                            description = "Other\n",
                            color = 0xFFB500)
    embed.set_author(name = message.author, icon_url = message.author.avatar_url)
    embed.set_footer(text = "click 1 to go back")
    
    embed.add_field(name = "Profile", value = "__**!profile**__ or __**!pf**__ to display all of your stats. \n__**!profile/!pf [username or nickname]**__ to display a user's profile")
    embed.add_field(name = "Nicknames", value = """__**!setname [name]**__ to change your nickname. \n__**!name**__ to check your nickname \nThis will be the name that
                                                    other users will use to trade with you and will be shown on leaderboards""")
    embed.add_field(name = "Leaderboard", value = "__**!lb**__ to show the bread leaderboard\n__**!gwins**__ to show the guessing game wins leaderboard")
    embed.add_field(name = "Support", value = """Owner: **hoody#9652**
                                                Moderator: **Blake | 10497#0510**
                                                [Bakery Server](https://discord.gg/ynFhHfWg9h)
                                                [Invite The Baker to another server!](https://discord.com/api/oauth2/authorize?client_id=416447447515267072&permissions=268495952&scope=bot)""")
    embed.add_field(name = "Tips", value = """Creating a text channel named __bakery-updates__ will allow updates and announcements to go there instead of #bakery
                                            \nThe most popular commands are **bake**, **!citygame**, **!flaggame**, and **start guessing**""")
    otherMenu = await menu.edit(embed = embed)
    await menu.add_reaction("1️⃣") #1
    previous_status = True
    def check(reaction, userName):
        return userName == message.author
    
    reaction, userName = await bot.wait_for('reaction_add', check=check)
    if (str(reaction) == "1️⃣"):
        await menu.clear_reactions()
        return
