import os.path
from os import path
import time
from datetime import datetime
import random
import DatabaseOperations
import Utilities


async def startGuessGame(user):
    userData = DatabaseOperations.getDataList(user) 
    canPlay, waitTime = Utilities.checkCooldown(user, "gg cooldown", 10)
    
    if (userData['gg answer'] != -1):
        response = "Guessing game is already active for " + str(user.author.name)
    elif (not canPlay):
        if (int(waitTime) > 1):
            response = "Cooldown is active. Wait time is " + str(waitTime) + " minutes"
        else:
            response = "Cooldown is active. Wait time is " + str(waitTime) + " minute"
    else:

        #pick a number between 1 and 15 for the user to guess
        winNumber = random.randrange(1, 16)
        userData['gg answer'] = winNumber

        #set available guesses to default (3)
        userData['gg avail guesses'] = 3

        userData['gg played'] += 1
        
        DatabaseOperations.writeToDB(userData) #send the user list and index, function will save to UserDatabase.txt
        
        response = "Guessing game has started for " + str(user.author.name) + ". Pick a number between 1 and 15"
        
    embed = await Utilities.getEmbedMsg(body_text = response)
    await user.channel.send(embed = embed)



async def readGuess(user, guess):
    userData = DatabaseOperations.getDataList(user)
    output = ""
    
    if (int(guess) > 15 or int(guess) < 1):
        output = "guess out of bounds. select a number between 1 and 15"
    else:
        if (guess == userData['gg answer']): #check if users guess is the winning number
            output = ":scream: you guessed the winning number! (" + str(userData['gg answer']) + ")\nYou win 3 bread boxes!"

            #add 3 boxes as reward for guessing correctly
            userData['bread box'] = userData['bread box'] + 3

            #add to # of guessing game wins
            userData['gg wins'] += 1
            
            userData['gg answer'] = -1
            
            #save the time finished so i can check cooldown
            userData['gg cooldown'] = Utilities.getTime()
        else:
            userData['gg avail guesses'] -= 1
            output = ":slight_frown: not the right number (" + str(userData['gg avail guesses']) + " guesses remaining)"
            if (userData['gg avail guesses'] <= 0):
                output += "\nYou are out of guesses! The number was " + str(userData['gg answer']) + ". You can start another game in 10 minutes"

                #save the time finished so i can check cooldown
                userData['gg cooldown'] = Utilities.getTime()
                
                userData['gg answer'] = -1

        
        

        DatabaseOperations.writeToDB(userData) #save all changes to the user's data in the database
    
    embed = await Utilities.getEmbedMsg(body_text = output)
    await user.channel.send(embed = embed)
    



def checkIfGuessGameActive(user):
    userData = DatabaseOperations.getDataList(user)
    return userData['gg answer']
