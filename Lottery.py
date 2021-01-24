import time
from datetime import datetime
import random
import os.path

import DatabaseOperations



def checkIfActive():
    activePredictions = os.path.join("Lottery/", "active-lottery.txt")    
    fileActivePrediction = open(activePredictions, "r")
    active = fileActivePrediction.readline()
    fileActivePrediction.close()

    return active

def checkJackpot():
    jackpotPath = os.path.join("Lottery/", "jackpot.txt")
    currentPotFile = open(jackpotPath, "r")
    pot = int(currentPotFile.readline())
    currentPotFile.close()

    return "Current jackpot: " + str(pot) + " bread boxes"


#set the active lottery file to true and give everyone 1 ticket
def startLotteryPredictions():
    activePredictions = os.path.join("Lottery/", "active-lottery.txt")
    
    if (checkIfActive() == "false"):
        fileActivePredictionW = open(activePredictions, "w")
        fileActivePredictionW.write("true")        
        fileActivePredictionW.close()
    
    with open('UserDatabase.txt', 'r') as file: #read the database file
        data = file.readlines()
    
    #set number of guesses to 1 for everyone so there is a minimum of 1 guess per person 
    for i in range(0, len(data) - 1):
        userData = DatabaseOperations.convertToDict(data[i])
        userData['donations'] = str(int(userData['donations']) + 10)
        DatabaseOperations.writeToDB(userData)
        
    return "predictions are active"




def checkTickets():
    ticketsList = ""
    
    if (checkIfActive() == "true"):
        userList = []
        
        with open("UserDatabase.txt") as f:
            data = f.readlines()
    
        ticketsList = "```css\n\t\t\t\t\tTICKETS\n"

        for i in range(0, len(data) - 1):
            userData = DatabaseOperations.convertToDict(data[i])
            userTickets = userData['ticket list'][1:]
            if (len(userTickets) > 0):
                ticketsList += "\n" + userData['name'][:-5] + ": " + userTickets
            
        ticketsList += "\n```"
    else:
        ticketsList = "there are no tickets right now"

    return ticketsList




def userPredict(user, userGuess):
    userData = DatabaseOperations.getDataList(user)
    response = ""
    active = checkIfActive()

    if (active == "false"):
        response = "Lottery is not active right now :)"
    elif (active == "true"):
        if (int(userGuess) > 0 and int(userGuess) <= 175):
            #check how much bread user has
            userPoints = int(userData['bread'])

            cost = 0

            totalTickets = len(userData['ticket list'].split(':')) - 1
            
            if (totalTickets >= 11):
                response = "you dont have any guesses remaining (donate to get more; 11 guesses max)"
            else:
                if (userPoints > 0):
                    if (userPoints < 10000): #cost is 1 bread for anyone less than 10k bread
                        cost = 1
                    elif (userPoints >= 10000): #cost is 0.01% of user's total bread for anyone above 10k bread
                        cost = userPoints * 0.0001

                    #update player points
                    userData['bread'] = str(int(userPoints - cost)) + "\n"
                    
                    #save user's guess                   
                    userData['ticket list'] += ":" + userGuess
                    
                    
                    response = str(user.author.name) + " has entered " + str(userGuess) + " as their lottery ticket " + "(cost: {:,} bread".format(int(cost)) + ")"
            
                    #add 7 bread boxes for each user that enters
                    jackpotPath = os.path.join("Lottery/", "jackpot.txt")
                    currentPotFile = open(jackpotPath, "r")
                    pot = int(currentPotFile.readline())
                    currentPotFile.close()
                
                    newPot = pot + 7

                    newPotFile = open(jackpotPath, "w")
                    newPotFile.write(str(newPot))
                    newPotFile.close()

                    DatabaseOperations.writeToDB(userData)
        else:
            response = "your number is out of range, choose a number between 1 and 175"
                       
    return response






def donateToJackpot(user, donation):
    userData = DatabaseOperations.writeToDB(user)
    response = ""

    donations = int(userData['donations'])
    
    if (donations > 110):
        response = "you have donated the max amount already"
    else:
        if (int(donation) < 1):
            response = "<:WeirdChamp:778827632053583872> you can't donate less than 1%"
        elif (int(donation) > 10):
            response = "<:WeirdChamp:778827632053583872> you can't donate more than 100% of your bread"
        else:
            #check how much bread user has
            userBread = int(userData['bread'])
        
            percentAmnt = int(userBread * (int(donation)/100)) #get the bread value of the % of their total
            userBread = int(userBread - percentAmnt) #subtract what they donated from their total bread
        
            #write new bread amount
            userData['bread'] = str(userBread) + "\n"
        
            breadBoxValue = int(donation) * 2 #bread box value is 2x the percent they donate. open to change
        
            #add boxes to jackpot
            jackpotPath = os.path.join("Lottery/", "Jackpot.txt")
            currentPotFile = open(jackpotPath, "r")
            pot = int(currentPotFile.readline())
            currentPotFile.close()
        
            newPotFile = open(jackpotPath, "w")
            newPotFile.write(str(pot + breadBoxValue))
            newPotFile.close()

            #save the amount they donated so it increases their chances in winning the lottery
            userData['donations'] = str(int(userData['donations']) + int(donation))

            DatabaseOperations.writeToDB(userData) #save changes to database

            
            response = "<:PogChamp:304416481528250369> " + str(user.author.name) + " donated " + str(breadBoxValue) + " bread boxes to the jackpot\nCost: -{:,} bread".format(int(percentAmnt))

    return response





def stopLottery():
    activePredictions = os.path.join("Lottery/", "active-lottery.txt")
    active = checkIfActive()
    response = ""
    
    if (active == "false"):
        response = "predicts are already inactive"
    else:
        file = open(activePredictions, "w")
        file.write("false")
        file.close()
        
        response = "predictions have closed"

    return response





    
def startLottery():
    active = checkIfActive()
    response = ""
    if (active == "false"):
        response = "lottery is not active right now"
    elif (active == "true"):
        jackpotPath = os.path.join("Lottery/", "jackpot.txt")
        userList = []
        
        #lotteryNum = random.randrange(1, 176) #jackpot number
        lotteryNum = 5
        winner = ""
        count = 0
        
        with open('UserDatabase.txt', 'r') as file: #read the database file
            data = file.readlines()
    
        for i in range(0, len(data) - 1):
            userData = DatabaseOperations.convertToDict(data[i])

            userTickets = userData['ticket list'].split(':')
            userTickets.pop(0)
            
            if (len(userTickets) > 0):
                for j in range(0, len(userTickets)):
                    print(userTickets[j])
                    if (int(userTickets[j]) == lotteryNum):
                        #get jackpot amount
                        currentPotFile = open(jackpotPath, "r")
                        pot = int(currentPotFile.readline())
                
                        winner = userData['name']
                        response = "<:PogU:771737926936559656> " + winner[:-5].upper() + " WON THE LOTTERY!!! (Winning number: " + str(lotteryNum) + ")\nPrize: " + str(pot) + " bread boxes"                           

                        #add prize to user's boxes
                        userData['bread box'] = str(int(userData['bread box']) + pot)

                        #set jackpot to 0
                        resetJackpot = open(jackpotPath, "w")
                        resetJackpot.write("0")
                        resetJackpot.close()


                userData['ticket list'] = '' #clear tickets
                userData['donations'] = '0' #clear donations
                
                DatabaseOperations.writeToDB(userData)
                
        if (winner == ""):
            response = "<:Sadge:761225325723123732> nobody guessed the winning number (" + str(lotteryNum) + ")"


    
        
    #set lottery status to inactive
    activePredictions = os.path.join("Lottery/", "active-lottery.txt")
    lotteryFile = open(activePredictions, "w")
    lotteryFile.write("false")
    lotteryFile.close()

    
    return response
