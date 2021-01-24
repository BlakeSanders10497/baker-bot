import os.path
from os import path
import time
from datetime import datetime
import random
import DatabaseOperations
import Utilities

# check if a user can play the guess game or not, returns true or false
def checkGuessGameCooldown(user, userData):
    prevTime = userData['gg cooldown'] #returns a string with time
    currTime = Utilities.getTime()

    canPlay = False 
    
    if (float(currTime) - float(prevTime) >= 10): #if current time is greater than previous time by more than 5 minutes
        canPlay = True
        
    return canPlay


def startGuessGame(user):
    userData = DatabaseOperations.getDataList(user) 
    status = userData['gg active']
    canPlay = checkGuessGameCooldown(user, userData)
    
    if (status == "true"):
        response = "Guessing game is already active for " + str(user.author.name)
    elif (not canPlay):
        prevTime = userData['gg cooldown']
        currTime = Utilities.getTime()
        waitTime = 10 - (float(currTime) - float(prevTime))
        if (waitTime > 1):
            response = "Cooldown is active. Wait time is " + str(waitTime)[:-2] + " minutes"
        else:
            response = "Cooldown is active. Wait time is " + str(waitTime)[:-2] + " minute"
    else:
        #set game status to true
        userData['gg active'] = 'true'

        #pick a number between 1 and 15 for the user to guess
        winNumber = random.randrange(1, 16)
        userData['gg answer'] = winNumber

        #set available guesses to default (3)
        userData['gg avail guesses'] = 3

        
        DatabaseOperations.writeToDB(userData) #send the user list and index, function will save to UserDatabase.txt
        
        response = "Guessing game has started for " + str(user.author.name) + ". Pick a number between 1 and 15"
        
    return response



def readGuess(user, guess):
    userData = DatabaseOperations.getDataList(user)
    status = userData['gg active']
    output = ""
    
    if (status != "true"):
        output = "guessing game is not active (do !start guessing first)"
    elif (int(guess) > 15 or int(guess) < 1):
        output = "guess out of bounds. select a number between 1 and 15"
    else:
        if (guess == int(userData['gg answer'])): #check if users guess is the winning number
            output = "<:PogU:771737926936559656> you guessed the winning number! (" + str(userData['gg answer']) + ")\nYou win 3 bread boxes!"

            #add 3 boxes as reward for guessing correctly
            userData['bread box'] = int(userData['bread box']) + 3

            #deactivate the game
            userData['gg active'] = 'false'

            #add to # of guessing game wins
            userData['gg wins'] = int(userData['gg wins']) + 1
            
            #save the time finished so i can check cooldown
            userData['gg cooldown'] = Utilities.getTime()
        else:
            availGuesses = int(userData['gg avail guesses'])
            availGuesses -= 1
            output = "<:Weird:568458482840502302> not the right number (" + str(availGuesses) + " guesses remaining)"
            if (availGuesses <= 0):
                output += "\nYou are out of guesses! The number was " + str(userData['gg answer']) + ". You can start another game in 10 minutes"

                #deactivate the game
                userData['gg active'] = 'false'

                #save the time finished so i can check cooldown
                userData['gg cooldown'] = Utilities.getTime()
        

        availGuesses = int(userData['gg avail guesses'])
        availGuesses -= 1
        userData['gg avail guesses'] = availGuesses

        DatabaseOperations.writeToDB(userData) #save all changes to the user's data in the database
        
    return output



def checkIfGuessGameActive(user):
    userData = DatabaseOperations.getDataList(user)
    return userData['gg active']
