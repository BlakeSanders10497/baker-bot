import os
import asyncio
import random
import discord
import DatabaseOperations
import Utilities
import time
import ctypes

async def startFlagGame(user, bot):
    await user.channel.edit(slowmode_delay=3) #3 second slowmode
    
    with open("FlagGame/flag-names.txt", "r") as f:
        title_tags = f.readlines()
    

    notFound = True
    #file names arent perfectly in numeric order, so if a file is not found, pick another 
    while (notFound):
        index = random.randint(8, 239)
        answer = title_tags[index - 8]
        imagePath = "FlagGame/Flags/flag-" + str(index) + ".jpg"
        try:
            await user.channel.send(file=discord.File(imagePath))
            notFound = False
        except:
            pass

    
    title_text = "Loading Flag Game for " + str(user.author.name)
    body_text = ""
    msg = await user.channel.send(embed = await Utilities.getEmbedMsg(title_text))
    
    
    options = []
    answerIndex = random.randint(0, 3) #select which index the answer will be in

    #create list of 4 options
    for i in range(0, 4): 
        if (i == answerIndex):
            options.append(answer)
        else:
            #make sure the bot doesnt pick the same city twice, which would show up twice as an option for the user
            flag = True
            while (flag):
                option = title_tags[random.randint(8, 239) - 8] #pick a number
                unused = True
                for j in range(0, len(options)): #loop through the current list of options
                    if (option == options[j] or option == answer): #if the city chosen is already in the list, unused is set to false
                        unused = False
                if (unused == True): #if there was no match in the options list, the option chosen is has not been picked yet
                    options.append(option) #add it to the options
                    flag = False #exit the loop so another random city can be picked
                    
    
    
    #add reactions to the message
    await msg.add_reaction("🇦") # A
    await msg.add_reaction("🇧") # B
    await msg.add_reaction("🇨") # C
    await msg.add_reaction("🇩") # D
    
    userData = DatabaseOperations.getDataList(user)
    userData['flaggame answer'] = answerIndex + 1
    userData['flaggame played'] += 1
    DatabaseOperations.writeToDB(userData)

    if (userData['nickname'] == ""):
        name = str(user.author.name)
    else:
        name = userData['nickname']
    
    #create new embed message with body and title (list of options)
    title_text = f"This flag belongs to... (25 seconds to answer)"
    body_text = f"```\n\nA) {options[0]}B) {options[1]}C) {options[2]}D) {options[3]}```"
    await msg.edit(embed = await Utilities.getEmbedMsg(title_text, body_text, user, userData))

    def check(reaction, userName):
        return userName == user.author

    try:
        reaction, userName = await bot.wait_for('reaction_add', timeout=25.0, check=check)
    except asyncio.TimeoutError: #if user ran out of time
        await user.channel.edit(slowmode_delay=0) #remove slowmode
        
        title_text = f":confused: you ran out of time to answer"
        body_text = ""
        await msg.edit(embed = await Utilities.getEmbedMsg(title_text, body_text, user, userData))

    else: #if user answered with a reaction
        await user.channel.edit(slowmode_delay=0) #remove slowmode on channel
        
        result = await readAnswer(reaction.message, user, reaction.emoji) #get result of their answer
        body_text += "\n" + result #alter body text
        await msg.edit(embed = await Utilities.getEmbedMsg(title_text, body_text, user, userData))





async def readAnswer(message, user, reaction):
    char_list = ['A', 'B', 'C', 'D']
    userData = DatabaseOperations.getDataList(user)
    
    if (str(reaction) == "🇦"):
        ans = 1
        
    elif (str(reaction) == "🇧"):
        ans = 2
        
    elif (str(reaction) == "🇨"):
        ans = 3
           
    elif (str(reaction) == "🇩"):
        ans = 4

        

    if (userData['nickname'] == ''):
        name = str(user.author.name)
    else:
        name = userData['nickname']
    
    if (ans == int(userData['flaggame answer'])): #check if user answer is correct
        #add reward
        userData['bread box'] += 1
        response = ":nerd: you win 1 bread box"
        userData['flaggame wins'] += 1
    else:
        response = ":no_entry_sign: the answer was " + char_list[userData['flaggame answer'] - 1]

    #reset game
    userData['flaggame answer'] = -1
    userData['flaggame cooldown'] = Utilities.getTime()

    DatabaseOperations.writeToDB(userData)
                
    return response



