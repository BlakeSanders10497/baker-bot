import discord
from discord.ext import commands
import asyncio
import random
import time
from datetime import datetime
import os.path
from os import path

#mine
import Leaderboard 
import GuessingGame 
import DatabaseOperations 
import Utilities 
import Lottery
import CityGame
import Store
import BreadBox
import FlagGame
import Bread


bot = commands.Bot(command_prefix='.', description='A bot that greets the user back.')
client = discord.Client()




async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')




        
async def testFunction(message):
    userData = DatabaseOperations.getDataList(message)
    print(message.roles)
    output = "```\nNAME: " + userData['name'] + "\nBread box purchases: "
    output += userData['bread box purchases'] + "\nBread boxes: " + userData['bread box'] +"\nCurrent donations: " 
    output += userData['donations'] + "\nGG Avail guesses: " + userData['gg avail guesses'] + "\nGG Cooldown: " 
    output += userData['gg cooldown'] + "\nGG Active: " + userData['gg active'] + "\nGG winning num: " 
    output += userData['gg answer'] + "\nGG wins: " +userData['gg wins'] + "\nLottery tickets: " 
    output += userData['ticket list'] + "\nNum of guesses: " + userData['num tickets'] + "\nBake cooldown: " 
    output += userData['timeout'] + "\nID: " + userData['id'] + "\nBread: " + userData['bread'] + "\n```"
    
    await message.channel.send(output)





async def announce():
    roleTag = "<@&772528254749245470>"
    channel = bot.get_channel(799697811448135701)
    message = roleTag + "\n\t\t\t\t <:PogU:771737926936559656> **NEW UPDATE** <:PogU:771737926936559656> \n\n**New features**:\n\n\t"
    message += "**Butter**: once used, baking will reward more bread than normal (check the store to buy)\n\t"
    message += "**Flag game**: !flaggame will start a game where you have to guess the country flag (reward is 2 bread boxes)\n\n\n"
    message += "**Changes:**\n\n\t**City game**: answer by reacting with the corresponding letter (no more command answer)\n\t"
    message += "**Bake**: baking now gives between 1 and 10 bread until you reach 1,000 bread, then it gives between 0.1%-1%\n\t"
    message += "**Bread boxes**: now cost 3% of your bread and will give between 1% and 8%\n\t"
    message += "**Gamble**: gambling is now even odds between losing or gaining bread"
    await channel.send(message)


async def helpMsg(message):

    me = await client.get_user_info(message.author.id)
    await client.send_message(me, "Hello!")


    
@bot.event
async def on_reaction_add(reaction, user):
    #userData = DatabaseOperations.getUserList(user)
    return



#==============================================================================================================================================================


@bot.event
async def on_message(message):  # event that happens per any message.
    breadLBPath = "Stats/bread leaderboard.png"
    winsLBPath = "Stats/wins leaderboard.png"

                
    print(f"{message.channel}: {message.author}: {message.author.name}: {message.author.id}: {message.content}")
    
    
    banned = False
    developer = False
    for i in range(0, len(message.author.roles)):
        if (str(message.author.roles[i]) == "Baked"): #user is banned if they have the Baked role
            banned = True
            print("player is banned")
        if (str(message.author.roles[i]) == "Developer"): #user is given high privileges if they have the Developer role
            developer = True
            print("player is a developer")


    if ((not banned and message.author.bot == False) or developer):


                    #developer commands
        if developer and "!!announce" in message.content:
            await announce()
            
        if developer == True and "!!test" in message.content.lower():
            await join(message)

        
        if str(message.channel) == "bakery" and str(message.content) == "!help":
            await helpMsg(message)
    
    
                            # BREAD COMMANDS
        #BAKE 
        elif str(message.channel) == "bakery" and str(message.content) != "!bakes" and "bake" in message.content.lower():
            canBake, waitTime = Utilities.checkCooldown(message, "timeout", 1)
            if (canBake):
                await message.channel.send(Bread.bake(message))
            else:
                await message.channel.send("you already baked :)")
    
        #check bread
        elif str(message.author) != "The Baker#0723" and str(message.channel) == "bakery" and "!bread" in message.content.lower():
            await Bread.checkLevel(message)
        
        
        #check bake count
        elif str(message.channel) == "bakery" and "!bakes" in message.content.lower():
            await message.channel.send(Utilities.checkBakeCount(message))
        
        #check gamble count
        elif str(message.channel) == "bakery" and str(message.content) == "!gcount":
            await message.channel.send(Utilities.checkGambleCount())
    
    
        
        #gamble EZ
        if  str(message.channel) == "bakery" and "!gamble" in message.content.lower():
            await Bread.gamble(message)
    
    
            
        #donate bread to another user
        if str(message.channel) == "bakery" and "!give" in message.content.lower():
            await Bread.giveBread(message)
    
    
        
    
    
        
    
    
        
    
                    # STORE COMMANDS
                    
        #open the store 
        if str(message.channel) == "bakery" and str(message.content.lower()) == "!store":
            await message.channel.send(Store.store(message))
    
        #buy an item
        if str(message.channel) == "bakery" and "!buy" in message.content.lower():
            msg = message.content.split()
            await Store.storePurchase(message, msg[1])
    
    
    
    
                        # BUTTER
        if str(message.channel) == "bakery" and str(message.content.lower()) == "!butter":
            await Store.getButterCount(message)

        if str(message.channel) == "bakery" and str(message.content.lower()) == "!use butter":
            await Store.useButter(message)
            
            
            
            
    
                    # BREAD BOX COMMANDS
        
        #open a bread box 
        if str(message.channel) == "bakery" and message.content.startswith("!open"):
            await message.channel.send(BreadBox.openBreadBox(message))
    
        
        #check how many boxes you have
        if str(message.channel) == "bakery" and str(message.content.lower()) == "!boxes":
            await message.channel.send(BreadBox.getBreadBoxCount(message))
        
        #check how many boxes you have left to buy today (15 max)
        if str(message.channel) == "bakery" and str(message.content.lower()) == "!boxlimit":
            await message.channel.send(BreadBox.getBoxPurchases(message))
    
    
        #give a user a bread box    
        if str(message.channel) == "bakery" and message.content.startswith("!trade"):
            await BreadBox.tradeBox(message)
    
    
    
    
    
    
                    # LOTTERY COMMANDS
                    
        #allow predictions to start
        if str(message.author) == "hoody#9652" and str(message.channel) == "bakery" and str(message.content.lower()) == "!start predictions":
            await message.channel.send(Lottery.startLotteryPredictions())
    
        #command for submitting a guess
        if str(message.channel) == "bakery" and "!ticket" in message.content.lower():
            msg = message.content.split()
            try: 
                userGuess = msg[1]
            except:
                await message.channel.send("enter a number to guess (between 1 and 200)")                       
            await message.channel.send(Lottery.userPredict(message, userGuess))
    
        #starts the lottery and checks if there's a winner
        if str(message.author) == "hoody#9652" and str(message.channel) == "bakery" and str(message.content.lower()) == "!start lottery":
            await message.channel.send("<:pausechamp:793988297637625958>")
            for i in range(0, 3):
                await message.channel.send("...\n")
                time.sleep(2)
            await message.channel.send(Lottery.startLottery())
    
        #check prizepool
        if str(message.channel) == "bakery" and "!prize" in message.content.lower():
            await message.channel.send(Lottery.checkJackpot())
    
        
        #donate to the jackpot
        if str(message.channel) == "bakery" and "!add" in message.content.lower():
            msg = message.content.split()
            try:
                donation = msg[1]
            except:
                await message.channel.send("enter a percentage to donate (e.g.: \"!add 1\" donates 1% of your bread)")
                                           
            await message.channel.send(Lottery.donateToJackpot(message, donation))
        
        
        if str(message.channel) == "bakery" and str(message.content) == "ticket list":
            await message.channel.send(Lottery.checkTickets())
    
        
        
    
    
                                # GUESSING GAME COMMANDS
        #start the guess game
        if str(message.channel) == "bakery" and str(message.content).lower() == "start guessing":
            await message.channel.send(GuessingGame.startGuessGame(message))
        
        #read a user's guess
        if str(message.channel) == "bakery" and str(message.author) != "The Baker#0723":
            if (GuessingGame.checkIfGuessGameActive(message) == "true"):
                try:
                    number = int(message.content)
                except:
                    print("failed to parse messange.content into int")
                try:    
                    await message.channel.send(GuessingGame.readGuess(message, number))
                except:
                    print("not a guess")






                            # CITY GAME COMMANDS
        if str(message.channel) == "bakery" and str(message.content.lower()) == "!citygame":
            canBake, waitTime = Utilities.checkCooldown(message, "citygame cooldown", 15)
            if (canBake):
                await CityGame.startCityGame(message, bot)
            else:
                await message.channel.send("cooldown is " + str(waitTime)[:-2] + " minutes")
        
    
    
    
    
    
    
                        # LEADERBOARD
        if str(message.channel) == "bakery" and str(message.content.lower()) == "!gwins":
            Leaderboard.makeLeaderboard("gg wins", winsLBPath)
            await message.channel.send(file=discord.File(winsLBPath))
    
        if  str(message.channel) == "bakery" and str(message.content.lower()) == "!lb":
            Leaderboard.makeLeaderboard("bread", breadLBPath)
            await message.channel.send(file=discord.File(breadLBPath))
    
    
    
                        
                        
                        # NICKNAMES
        if str(message.channel) == "bakery" and message.content.startswith("!setname"):
            await setNickname(message)
        
        if str(message.channel) == "bakery" and str(message.content.lower()) == "!name":
            await checkNickname(message)




    
                        # FLAG GAME
        if str(message.channel) == "bakery" and str(message.content.lower()) == "!flaggame":
            canBake, waitTime = Utilities.checkCooldown(message, "flaggame cooldown", 10)
            if (canBake):
                await FlagGame.startFlagGame(message, bot)
            else:
                await message.channel.send("cooldown is " + str(waitTime)[:-2] + " minutes")
    
    
    
    
        

        
        #useless function that responds when a user @'s it
        if str(message.channel) == "bakery" and "<@!416447447515267072>" in message.content:
            await message.channel.send("dont @ me")
            
            
    else:
        if (message.author.bot == True):
            pass
        else:
            await message.channel.send("you are not allowed in the bakery")


    if ("<@&747923936829898952>" in message.content):
        await message.add_reaction("<:DonoWall:773327472644063253>")


tokenPath = os.path.join("token.txt")
file = open(tokenPath, "r")
token = file.readline()
file.close()

bot.run(token)







'''

dictionary keys
['nickname', 'name', 'bread box purchases', 'bread box', 'butter', 'butter purchases', 
 'butter life', 'donations', 'gg avail guesses', 'gg cooldown', 'gg active', 'gg answer', 
 'gg wins', 'ticket list', 'num tickets', 'citygame cooldown', 'citygame answer', 
 'flaggame cooldown', 'flaggame answer', 'timeout', 'id', 'bread']


(OLD)
userData elements and their indicies 

name = 0
bread box purchases = 1
bread box = 2
current donations = 3
guess game available guesses = 4
guess game cooldown = 5
guess game status = 6
guess game winning number = 7
guess game wins = 8
lottery guess = 9
number of guesses = 10
timeout = 11
user ID = 12
bread = 13

'''






#      roles
# <@&747923936829898952> @among us (ping) role

#      emotes
# <:EZ:406827146632232972> 
# <:OMEGALUL:420884833288454163> 
# <:monkaS:384078011366113280>
# <:squadw:771036304874930178>
# <:KermitTea:303786824831336448>
# <:pepelaugh:771033359837036564>
# <:FeelsBadMan:303787556213096458>
# <:MEGALUL:761218566132334622>
# <:angry_pepe:406826858139746313>
# <:Weird:568458482840502302>
# <:emoji_27:608818423430119454> Pepe holding knife
# <:Sadge:761225325723123732>
# <:PogChamp:304416481528250369>
# <:FeelsAmazingMan:400752334856126465>
# <:5Head:771067313738481674>
# <:stonks:761227625423044629>
# <:PogU:771737926936559656>
# <:FeelsGoodMan:452068213665300490>
# <:peepofat:775341285544427561>
# <:WeirdChamp:778827632053583872>
# <:pausechamp:793988297637625958>
# <:FeelsWeirdMan:783529533206822942>
