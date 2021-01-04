import os.path
import matplotlib.pyplot as plt


def leaderboard():
    completeName = os.path.join("User levels/", ",List of Account names.txt")
    file = open(completeName, "r")
    userList = []
    userList = file.readline().split(',') #list of each user's name that has bread
    file.close()
    
    pointsList = getUserPointsList(userList) #list of each user's points

    temp = 0
    tempName = ""

    #insertion sort algorithm
    for i in range(0, len(userList)):
        j = i
        
        while (j > 0 and pointsList[j] < pointsList[j - 1]): #if the number before the current number is lower, true
            temp = pointsList[j]
            tempName = userList[j]

            #swap numeric values
            pointsList[j] = pointsList[j - 1]
            pointsList[j - 1] = temp

            #swap names so that the indicies of each list (name and points) match
            userList[j] = userList[j - 1]
            userList[j - 1] = tempName
            
            j -= 1
            
        i += 1



    plt.style.use("ggplot")

    #create a list of the bread value in exponent form (e.g.: 10^x)
    breads = []
    for j in range(0, len(pointsList)):
        breads.append(len(str(pointsList[j])) - 1)

    #create a list of usernames without the tag (e.g.: subscript #1111 away)
    names = []
    for k in range(0, len(userList)):
        names.append(userList[k][:-5])

    x_pos = [i for i, _ in enumerate(names)]
    
    plt.barh(x_pos, breads, color = 'blue') #create a horizontal bar graph
    plt.ylabel("Users") #y label is users
    plt.xlabel("Amount of bread (10^x)") #x label is bread
    plt.title("LEADERBOARD") 
    plt.yticks(x_pos, names) #place usernames
    plt.savefig('leaderboard.png', bbox_inches = 'tight', pad_inches = 0.1) #save graph

    
    return 'leaderboard.png'




def getUserPointsList(userList):
    userPointsList = []
    
    for count in range(0, len(userList)):
        userPath = os.path.join("User levels/", userList[count] + ".txt")
        userFile = open(userPath, "r")
        userPoints = int(userFile.readline())
        userPointsList.append(userPoints)

    return userPointsList
