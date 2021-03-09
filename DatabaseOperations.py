import os.path
import Utilities
import json


def getDatabase():
    with open('util/Database.json', 'r') as file: #read the database file
        data = json.load(file)
    
    return data

def saveDatabase(data):
    with open('util/Database.json', 'w') as file:
        json.dump(data, file, indent = 4)


def getDataList(user):
    """
    Receive the user's dictionary by using their id as a key. If not found,
    add a new dictionary to the database
    
    param: discord Message object
    return: dictionary of user's data
    """
    data = getDatabase()
    
    try:
        userData = data[str(user.author.id)]
    except:
        print("adding new user to database (error on DatabaseOperations.py line 28)")
        userData = addNewUser(user)
    
    return userData




#write the user's data to the database
def writeToDB(userData):
    """
    Write to the database by getting the location of the user's data, and overwriting their previous info
    
    Parameter: dictionary of a user's data
    """
    data = getDatabase()
    
    try:
        data[str(userData['id'])] = userData #save in the database list
    except:
        print("Error placing userData in database (DatabaseOperations line 48)")


    saveDatabase(data)


    


#create a new line in the database file and add default information of a new user
def addNewUser(user):
    """
    Create a new spot in the database with default values for the new user. 
    The user's id will be the key to access their dictionary
    
    param: discord Message object
    returns the new user's data as a dict
    """
    userData = {"nickname":"",
                "name":f"{user.author}",
                "bread box purchases":0,
                "bread box":0,
                "butter":0,
                "butter purchases":0,
                "butter life":0,
                "gg donations":0,
                "gg avail guesses":0,
                "gg cooldown":-10,
                "gg answer":-1,
                "gg played":0,
                "gg wins":0,
                "ticket list":"",
                "num tickets":0,
                "citygame cooldown":-15,
                "citygame answer":-1,
                "citygame played":0,
                "citygame wins":0,
                "flaggame cooldown":-10,
                "flaggame answer":-1,
                "flaggame played":0,
                "flaggame wins":0,
                "daily bakes":0,
                "bakes":0,
                "timeout":-1,
                "id":user.author.id,
                "bread":0}
    
    data = getDatabase()

    data[str(user.author.id)] = userData

    saveDatabase(data)
        
    
    return userData




def searchUserByNickname(nickname):
    """
    Check database only for nickname
    
    param: string
    returns the user's data as a dict if found, else, returns empty dict
    """
    data = getDatabase()
        
    userData = {}
    keys = list(data.keys())
    for id in keys:
        if (str(nickname).lower() == data[id]['nickname'].lower()):
            userData = data[id]

    return userData

def searchUserByUsername(username):
    """
    Check database only for username
    
    param: string (discord username e.g.: The Baker#0001)
    returns the user's data as a dict if found, else, returns empty dict
    """
    data = getDatabase()
        
    userData = {}
    keys = list(data.keys())
    for id in keys:
        if (str(nickname).lower() == data[id]['name'].lower()):
            userData = data[id]

    return userData


def searchUser(username):
    """
    Check if the string username is equal to (not case sensitive) a username or nickname in the database
    
    param: string
    returns that user's data as a dict and found as True if found, if not, the dict is empty and found is False
    """
    data = getDatabase()
    
    found = False
    userData = {}
    keys = list(data.keys())
    
    for id in keys:
        if (str(username).lower() == data[id]['nickname'].lower() or str(username).lower() == data[id]['name'].lower()):
            userData = data[id]
            found = True

    return userData, found
    


def looseSearch(username):
    """
    Check if the string username is found anywhere in the database, checking
    nicknames and usernames using the find() function
    
    param: string
    returns that user's data as a dictionary, and the whether it was found as a bool
    """
    data = getDatabase()
    
    found = False
    userData = {}
    keys = list(data.keys())
    
    for id in keys:
        if (data[id]['name'].lower().find(str(username).lower()) != -1 or data[id]['nickname'].lower().find(str(username).lower()) != -1):
            userData = data[id]
            found = True

    return userData, found


