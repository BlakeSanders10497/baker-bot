# check if a user can play the guess game or not, returns true or false
def checkGuessGameCooldown(userName):
    prevTime = getPrevGuessGameTime(userName) #returns a string with time
    currTime = getTime()

    canPlay = False 
    
    if (float(currTime) - float(prevTime) >= 10): #if current time is greater than previous time by more than 5 minutes
        canPlay = True
        
    return canPlay


#retrieve the previous time a user played the guessing game
def getPrevGuessGameTime(userName):
    pathName = os.path.join("User levels/", userName + " guess game cooldown.txt")
    
    if (not path.exists(pathName)):
        fileW = open(pathName, "w")
        fileW.write("0")
        fileW.close()
        prevTime = 0
    else:
        fileR = open(pathName, "r")
        prevTime = float(fileR.readline())
    
    
    return prevTime



def checkIfGuessGameActive(statusPath):
    if (not path.exists(statusPath)):
        gameActivate = open(statusPath, "w")
        gameActivate.write("false")
        gameActivate.close()
        status = "false"
    else:
        gameActive = open(statusPath, "r")
        status = gameActive.readline()
        gameActive.close()

    return status
    


def startGuessGame(user, userPath):
    response = ""
    userGuessPath = os.path.join("User levels/", user + " guess game status.txt")
    status = checkIfGuessGameActive(userGuessPath)

    canPlay = checkGuessGameCooldown(user)
    
    if (status == "true"):
        response = "Guessing game is already active for " + user[:-5]
    elif (not canPlay):
        prevTime = getPrevGuessGameTime(user)
        currTime = getTime()
        waitTime = 10 - (float(currTime) - float(prevTime))
        if (waitTime > 1):
            response = "Cooldown is active. Wait time is " + str(waitTime)[:-2] + " minutes"
        else:
            response = "Cooldown is active. Wait time is " + str(waitTime)[:-2] + " minute"
    else:
        #check if they are in the list of users who have played already, if not, add them
        with open("Other files/guessing game user list.txt") as f:
            userList = f.readline().split(",")
        found = False
        for i in range(len(userList)):
            if (user == userList[i]):
                found = True
        if (not found):
            guessListPath = os.path.join("Other files/", "guessing game user list.txt")
            fileW = open(guessListPath, "w")
            fileW.write(str(user))
            fileW.close()
        
        #set game status to true
        gameActivate = open(userGuessPath, "w")
        gameActivate.write("true")
        gameActivate.close()

        #pick a number between 1 and 20 for the user to guess
        computerNumPath = os.path.join("User levels/", user + " guess game winning number.txt")
        numberFile = open(computerNumPath, "w")
        winNumber = random.randrange(1, 16)
        numberFile.write(str(winNumber))
        numberFile.close()

        #set available guesses to default (3)
        availableGuessPath = os.path.join("User levels/", user + " guess game available guesses.txt")
        availGuessFile = open(availableGuessPath, "w")
        availGuessFile.write(str(3))
        availGuessFile.close()

        response = "Guessing game has started for " + str(user)[:-5] + ". Pick a number between 1 and 15"
        
    return response


#retrieve the number of available guesses a user has
def getAvailableGuesses(user):
    availableGuessPath = os.path.join("User levels/", user + " guess game available guesses.txt")
    availGuessFile = open(availableGuessPath, "r")
    availGuesses = int(availGuessFile.readline())
    availGuessFile.close()
    
    return availGuesses



def readGuess(user, guess):
    guessStatusPath1 = os.path.join("User levels/", user + " guess game status.txt")
    status = checkIfGuessGameActive(guessStatusPath1)
    output = ""
    
    if (status != "true"):
        output = "guessing game is not active (do !start guessing first)"
    elif (int(guess) > 15 or int(guess) < 1):
        output = "guess out of bounds. select a number between 1 and 15"
    else:
        computerNumPath = os.path.join("User levels/", user + " guess game winning number.txt")
        winFile = open(computerNumPath, "r")
        winningNum = int(winFile.readline())
        winFile.close()

        if (guess == winningNum):
            userBreadBoxPath = os.path.join("User levels/", user + " Bread box.txt")
            checkBreadBoxPath(user)
            output = "<:PogU:771737926936559656> you guessed the winning number! (" + str(winningNum) + ")\nYou win 3 bread boxes!"

            #add 3 boxes as reward for guessing right
            fileBreadBoxR = open(userBreadBoxPath, "r")
            userBoxes = int(fileBreadBoxR.readline())
            fileBreadBoxR.close()

            userBoxes += 3

            fileBreadBoxW = open(userBreadBoxPath, "w")
            fileBreadBoxW.write(str(userBoxes))
            fileBreadBoxW.close()

            #deactivate the game
            guessStatusPath = os.path.join("User levels/", user + " guess game status.txt")
            gameDeactivate = open(guessStatusPath, "w")
            gameDeactivate.write("false")
            gameDeactivate.close()

            #add to # of guessing game wins
            guessWinsPath = os.path.join("User levels/", user + " guess game wins.txt")
            winsFile = open(guessWinsPath, "r")
            wins = int(winsFile.readline())
            winsFile.close()

            wins += 1

            winsFileW = open(guessWinsPath, "w")
            winsFileW.write(str(wins))
            winsFileW.close()
            
            #save the time finished so i can check cooldown
            currTime = getTime()
            completeName = os.path.join("User levels/", user + " guess game cooldown.txt")
            file = open(completeName, "w")
            file.write(str(currTime)) #send the current time because it is now the previous time
            file.close()
        else:
            availGuesses = getAvailableGuesses(user)
            availGuesses -= 1
            output = "<:Weird:568458482840502302> not the right number (" + str(availGuesses) + " guesses remaining)"
            if (availGuesses <= 0):
                output += "\nYou are out of guesses! The number was " + str(winningNum) + ". You can start another game in 10 minutes"

                guessStatusPath = os.path.join("User levels/", user + " guess game status.txt")
                gameDeactivate = open(guessStatusPath, "w")
                gameDeactivate.write("false")
                gameDeactivate.close()

                #save the time finished so i can check cooldown
                currTime = getTime()
                completeName = os.path.join("User levels/", user + " guess game cooldown.txt")
                file = open(completeName, "w")
                file.write(str(currTime)) #send the current time because it is now the previous time
                file.close()
        

        availGuesses = getAvailableGuesses(user)
        availGuesses -= 1
        
        

        availableGuessPath = os.path.join("User levels/", user + " guess game available guesses.txt")
        availGuessFileW = open(availableGuessPath, "w")
        availGuessFileW.write(str(availGuesses))
        availGuessFileW.close()
                
    return output