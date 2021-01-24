import os.path
import Utilities

def getDataList(user):
    with open('UserDatabase.txt', 'r') as file: #read the database file
        data = file.readlines()
        
    found = False #flag for whether the user is found in the database
    for i in range(0, len(data)):
        dataLine = convertToDict(data[i])
        if (dataLine['id'] == str(user.author.id)): #check if the user who baked is in the database
            userData = convertToDict(data[i])
            found = True
            
    if (found == False): #user wasnt found in the database
        userData = addNewUser(user)
        
    return userData


#take a dictionary and convert the values into a comma separated string
def convertToString(userData):
    strUserData = ""
    index = 0
    for value in userData.values():
        if (index == len(userData) - 1):
            strUserData += str(value)
        else:
            strUserData += str(value) + ","

        index += 1

    return strUserData


#write the user's data to the database
def writeToDB(userData):
    with open('UserDatabase.txt', 'r') as file: #read the database file
        data = file.readlines()

    index = getIndex(userData)
    strUserData = convertToString(userData) #convert user line to string
    
    try:
        data[index] = strUserData #save in the database list
    except:
        print("Error when placing strUserData line in data. index: " + str(index))


    with open('UserDatabase.txt', 'w') as file: #write it to the local file
        file.writelines(data)


#return the user's list of data. used only when you need to read data, not write
def getUserList(user):
    with open('UserDatabase.txt', 'r') as file: #read the database file
        data = file.readlines()
    
    userData = {}
    found = False #flag for whether the user is found in the database
    for i in range(0, len(data)):
        dataLine = convertToDict(data[i])
        if (str(dataLine['id']) == str(user.id)): #check if the user who baked is in the database
            userData = convertToDict(data[i])
            found = True

    return userData
    

#get which line (index) the user's data is on in UserDatabase.txt 
def getIndex(userData):
    with open('UserDatabase.txt', 'r') as file: #read the database file
        data = file.readlines()

    index = 1000 #set the index high so it will raise an error if not found
    for i in range(0, len(data) - 1):
        dataLine = convertToDict(data[i]) #get ID of the current line
        if (userData["id"] == dataLine['id']):
            index = i
            
    return index


#create a new line in the database file and add default information of a new user
def addNewUser(user):
    #create a string of default values (and user name and ID)
    strUserData = ",".join(["", str(user.author), '0', '0', '0', '0', '0', '0', '0', '-10', 'false', '0', '0', "", '0', '-15', '-1', '-15', '-1', '-1', '0', '0', str(user.author.id), '0\n'])

    with open('UserDatabase.txt', 'r') as file: #read the database file
        data = file.readlines()

    data.append(strUserData) #add to list of user data lines

    with open('UserDatabase.txt', 'w') as file: #write it to the local file
        file.writelines(data)
        
        
    userData = convertToDict(strUserData)
    
    return userData


#convert a string with comma-separated values into a dictionary 
def convertToDict(userDataLine):
    dataTypes = ['nickname', 'name', 'bread box purchases', 'bread box', 'butter', 'butter purchases', 'butter life', 'donations', 'gg avail guesses', 'gg cooldown', 'gg active', 'gg answer', 'gg wins', 'ticket list', 'num tickets', 'citygame cooldown', 'citygame answer', 'flaggame cooldown', 'flaggame answer', 'daily bakes', 'bakes', 'timeout', 'id', 'bread']
    userIndex = 0
    line = userDataLine.split(',')
    userData = {}
    for i in line:
        try:
            val = line[userIndex]
            userData[dataTypes[userIndex]] = val
        except:
            print("error creating the user dictionary in DatabaseOperations.convertToDict() for " + userData['name'])
        userIndex += 1
    
    return userData


def searchUserByNickname(nickname):
    with open('UserDatabase.txt', 'r') as file: #read the database file
        data = file.readlines()
        
    userData = {}
    
    for i in range(0, len(data) - 1):
        dataLine = convertToDict(data[i]) #get ID of the current line
        if (str(nickname).lower() == dataLine['nickname'].lower()):
            userData = dataLine

    return userData

def searchUserByUsername(username):
    with open('UserDatabase.txt', 'r') as file: #read the database file
        data = file.readlines()
        
    userData = {}
    
    for i in range(0, len(data) - 1):
        dataLine = convertToDict(data[i]) #get ID of the current line
        if (str(username).lower() == dataLine['name'].lower()):
            userData = dataLine

    return userData

def searchUser(username):
    with open('UserDatabase.txt', 'r') as file: #read the database file
        data = file.readlines()
        
    userData = {}
    found = False
    
    for i in range(0, len(data) - 1):
        dataLine = convertToDict(data[i]) #get ID of the current line
        if (str(username).lower() == dataLine['name'].lower()):
            userData = dataLine
            found = True
        elif (str(username).lower() == dataLine['nickname'].lower()):
            userData = dataLine
            found = True
            
    return userData, found
