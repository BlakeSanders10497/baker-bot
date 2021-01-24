import requests
from bs4 import BeautifulSoup as bs
import os
import asyncio
import random
import discord
import DatabaseOperations
import Utilities
import time

async def startFlagGame(user, bot):
    
    await user.channel.send("Loading Flag Game for " + str(user.author.name))

    #url = 'https://unsplash.com/s/photos/flag'
    urls = ['https://www.united-states-flag.com/world.html']


    # download page for parsing
    page = requests.get(urls[0])
    soup = bs(page.text, 'html.parser')

    # locate all elements with image tag
    image_tags = soup.find_all('img')

    #make a list of the city names
    raw_title_tags = soup.find_all(class_="home-titles")
    title_tags = []
    for i in range(0, len(raw_title_tags)): 
        title_tags.append(str(raw_title_tags[i])[24:-5])


    

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
            notFound = True

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
    
    text = "```This flag belongs to... (15 seconds to answer)\n\nA) " + options[0] + "\nB) " + options[1] + "\nC) " + options[2] + "\nD) " + options[3] + "\n```"
    #await user.channel.send(text)

    msg = await user.channel.send(text)
    
    #add reactions to the message
    await msg.add_reaction("🇦")
    await msg.add_reaction("🇧")
    await msg.add_reaction("🇨")
    await msg.add_reaction("🇩")



    userData = DatabaseOperations.getDataList(user)
    userData['flaggame answer'] = str(answerIndex + 1)
    DatabaseOperations.writeToDB(userData)

    def check(reaction, userName):
        return userName == user.author

    try:
        reaction, userName = await bot.wait_for('reaction_add', timeout=15.0, check=check)
    except asyncio.TimeoutError:
        await user.channel.send(f'<:Sadge:761225325723123732> {user.author.name} ran out of time to answer')
    else:
        await readAnswer(reaction.message, user.author, reaction.emoji)


async def readAnswer(message, user, reaction):
    char_list = ['A', 'B', 'C', 'D']
    userData = DatabaseOperations.getUserList(user)
    
    if (str(reaction) == "🇦"):
        ans = 1
        
    elif (str(reaction) == "🇧"):
        ans = 2
        
    elif (str(reaction) == "🇨"):
        ans = 3
           
    elif (str(reaction) == "🇩"):
        ans = 4

        

    if (userData['nickname'] == ''):
        name = user.name
    else:
        name = userData['nickname']
    
    if (ans == int(userData['flaggame answer'])): #check if user answer is correct
        #add reward
        userData['bread box'] = str(int(userData['bread box']) + 1)
        response = "(" + name + ") <:PogU:771737926936559656> you win 1 bread box"
    else:
        response = "(" + name + ") <:FeelsWeirdMan:783529533206822942> the answer was " + char_list[int(userData['flaggame answer']) - 1]

    #reset game
    userData['flaggame answer'] = '-1'
    userData['flaggame cooldown'] = Utilities.getTime()

    DatabaseOperations.writeToDB(userData)
            
    await message.channel.send(response)











    
def downloadImages():
    #2 websites where u can get images from
    urls = ['https://www.cntraveler.com/galleries/2016-01-08/the-50-most-beautiful-cities-in-the-world',
        'https://www.timeout.com/things-to-do/best-cities-in-the-world']

    # download page for parsing
    page = requests.get(urls[0])
    soup = bs(page.text, 'html.parser')

    # locate all elements with image tag
    image_tags = soup.find_all('img')

    # create directory for model images
    if not os.path.exists('CityGame'):
        os.makedirs('CityGame')

    # move to new directory
    os.chdir('images')

    # image file name variable
    x = 0
    url = 0
    # writing images
    for image in image_tags:
        try:
            url = image['src']
            response = requests.get(url)
            if response.status_code == 200:
                with open('cities-' + str(x) + '.jpg', 'wb') as f:
                    f.write(requests.get(url).content)
                    f.close()
                    x += 1
        except:
            print("error")





