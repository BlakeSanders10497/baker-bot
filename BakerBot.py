import discord
from discord.ext import commands
import asyncio
import random
import time
from datetime import datetime
import os.path
from os import path
import shutil
import subprocess
import logging

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



@bot.event
async def on_ready():
    print('Awake')
    await bot.change_presence(activity = discord.Game(name = f"on {len(bot.guilds)} servers!"))
    




@bot.event
async def on_guild_join(guild):
    original_directory = os.getcwd() #get directory of Bakerbot.py
    os.chdir("..") #go back one directory
    directory = str(os.getcwd()) #get that directory name
    time.sleep(random.random()) #sleep for a random amount of time so that the programs dont run the bot at the same time
    if (not path.exists(directory + f"/{guild.name} {guild.id}")): #check if a new folder for the server has been made
        original_folder = directory + "/blank-slate" #get the name of the folder I need to copy
        new_folder = directory + f"/{guild.name} {guild.id}" #create the name of the folder after the server name and ID
        try:
            destination = shutil.copytree(original_folder, new_folder) #create a copy of the blank-slate folder
        except:
            pass
        
        os.chdir(new_folder)
        
        subprocess.Popen(['xterm', '-e', 'python3 BakerBot.py']) #open new terminal and run the bot for that server
        
        channel = discord.utils.get(bot.get_all_channels(), guild__name = guild.name, name="bakery")
        if (channel == None):
            channel = await guild.create_text_channel('bakery') #create bakery channel
    
        embed = await Utilities.getEmbedMsg(body_text = "```fix\nWelcome to the bakery, pastry chefs!```", footer_text = "type !help for commands")
        await channel.send(embed = embed)
        
    os.chdir(original_directory) #change directory back to the folder the bot is located in
    
    



#==============================================================================================================================================================


@bot.event
async def on_message(message):  # event that happens per any message.
    breadLBPath = "Stats/bread leaderboard.png"
    winsLBPath = "Stats/wins leaderboard.png"
    cwd = os.getcwd()
    
    
    banned = False
    developer = False
    for i in range(0, len(message.author.roles)):
        if (str(message.author.roles[i]) == "Baked"): #user is banned if they have the Baked role
            banned = True
        if (str(message.author.roles[i]) == "Developer"): #user is given high privileges if they have the Developer role
            developer = True

    if (str(message.channel) == "bakery"): #make sure the message is from a channel named "bakery"
        
        if (str(cwd).find(str(message.guild.id)) != -1): #find if the server name is located in the directory of this program
    
            
            # announcement command
            if (str(message.author) == "hoody#9652" and message.content.startswith("!!announce")): 
                try:
                    server_id = int(message.content.split('::')[1])
                except: #server id is optional in the command, so continue if there is no id
                    server_id = -1
                try:
                    announcement = f"```fix\n{message.content.split('::')[2]}```" #get all text past the ::
                except IndexError:
                    await message.channel.send("```!!announce ::[server id] (optional):: [message]```")
                else:
                    new_embed = await Utilities.getEmbedMsg("", announcement) #create embed message
                    await message.channel.send(embed=new_embed)
                    await message.channel.send("are you sure you want to make the announcement? (!!confirm)")
                    def check(m):
                        return m.content == "!!confirm"
                    try:
                        msg = await bot.wait_for("message", timeout = 30, check=check) #give myself 30 seconds to confirm the announcement
                    except asyncio.TimeoutError:
                        await message.channel.send("timed out") #otherwise timeout
                    else:
                        if server_id == -1:
                            server_id_list = list(bot.guilds) #create list of servers the bot is in
                            for server in server_id_list: #traverse through list of servers
                                channel = discord.utils.get(bot.get_all_channels(), guild__name = str(server.name), name="bakery-updates")
                                if (channel == None):
                                    channel = discord.utils.get(bot.get_all_channels(), guild__name = str(server.name), name="bakery") #get bakery channel in the server
                                await channel.send(embed=new_embed) #send the announcement to the server
                        else:
                            channel = discord.utils.get(bot.get_all_channels(), guild__name = bot.get_guild(server_id).name, name="bakery")
                            await channel.send(embed=new_embed)
    
    
    
            if (developer or (not banned and message.author.bot == False)): #make sure user is not a bot and not banned (unless they are a developer)
                print(f"{message.guild.name}: {message.channel}: {message.author}: {message.content}")
                            #developer commands
                if developer and "!!announce" in message.content:
                    #await announce()
                    pass
                    
                if developer == True and "!!test" in message.content.lower():
                    Utilities.resetTime()
        
                
                if str(message.content) == "!help":
                    await Utilities.helpMenu(bot, message)
            
            
                                    # BREAD COMMANDS
                #BAKE 
                elif message.content.lower().startswith("bake"):
                    canBake, waitTime = Utilities.checkCooldown(message, "timeout", 1)
                    if (canBake):
                        await Bread.bake(message)
                    else:
                        body = "cooldown is less than a minute"
                        embed = await Utilities.getEmbedMsg(body_text = body)
                        await message.channel.send(embed = embed)
            
                #check bread
                elif "!bread" in message.content.lower():
                    await Bread.checkLevel(message)
                
                
                #check bake count
                elif "!bakes" in message.content.lower():
                    await message.channel.send(Utilities.checkBakeCount(message))
                
                #check gamble count
                elif str(message.content) == "!gcount":
                    await message.channel.send(Utilities.checkGambleCount())
            
            
                
                #gamble EZ
                elif message.content.lower().startswith("!gamble"):
                    await Bread.gamble(message)
            
            
                    
                #donate bread to another user
                elif message.content.lower().startswith("!give"):
                    await Bread.giveBread(message, bot)
            
            
                
            
            
                
            
            
                
            
                            # STORE COMMANDS
                            
                #open the store 
                elif str(message.content.lower()) == "!store":
                    await Store.store(message)
            
                #buy an item
                elif message.content.lower().startswith("!buy"):
                    msg = message.content.split()
                    await Store.storePurchase(message, msg[1])
            
            
            
            
                                # BUTTER
                elif str(message.content.lower()) == "!butter":
                    await Store.getButterCount(message)
        
                elif str(message.content.lower()) == "!use butter":
                    await Store.useButter(message)
                    
                    
                    
                    
            
                            # BREAD BOX COMMANDS
                
                #open a bread box 
                elif message.content.startswith("!open"):
                    await BreadBox.openBreadBox(message)
            
                
                #check how many boxes you have
                elif str(message.content.lower()) == "!boxes":
                    await message.channel.send(BreadBox.getBreadBoxCount(message))
                
                #check how many boxes you have left to buy today (5 max)
                elif str(message.content.lower()) == "!boxlimit":
                    await message.channel.send(BreadBox.getBoxPurchases(message))
            
            
                #give a user a bread box    
                elif message.content.startswith("!trade"):
                    await BreadBox.tradeBox(message, bot)
            
            
            
            
            
            
                            # LOTTERY COMMANDS
                            
                #allow predictions to start
                elif str(message.author) == "hoody#9652" and  str(message.content.lower()) == "!start predictions":
                    await message.channel.send(Lottery.startLotteryPredictions())
            
                #command for submitting a guess
                elif "!ticket" in message.content.lower():
                    msg = message.content.split()
                    try: 
                        userGuess = msg[1]
                    except:
                        await message.channel.send("enter a number to guess (between 1 and 200)")                       
                    await message.channel.send(Lottery.userPredict(message, userGuess))
            
                #starts the lottery and checks if there's a winner
                elif str(message.author) == "hoody#9652" and  str(message.content.lower()) == "!start lottery":
                    for i in range(0, 3):
                        await message.channel.send("...\n")
                        time.sleep(2)
                    await message.channel.send(Lottery.startLottery())
            
                #check prizepool
                elif "!prize" in message.content.lower():
                    await message.channel.send(Lottery.checkJackpot())
            
                
                #donate to the jackpot
                elif "!add" in message.content.lower():
                    msg = message.content.split()
                    try:
                        donation = msg[1]
                    except:
                        await message.channel.send("enter a percentage to donate (e.g.: \"!add 1\" donates 1% of your bread)")
                                                   
                    await message.channel.send(Lottery.donateToJackpot(message, donation))
                
                
                elif str(message.content) == "ticket list":
                    await message.channel.send(Lottery.checkTickets())
            
                
            
        
        
        
        
                                    # CITY GAME COMMANDS
                elif str(message.content.lower()) == "!citygame":
                    canBake, waitTime = Utilities.checkCooldown(message, "citygame cooldown", 15)
                    if (canBake):
                        await CityGame.startCityGame(message, bot)
                    else:
                        if (int(waitTime) == 1):
                            body = "cooldown is " + waitTime + " minute"
                        else:
                            body = "cooldown is " + waitTime + " minutes"
                        embed = await Utilities.getEmbedMsg(body_text = body)
                        await message.channel.send(embed = embed)
                
            
            
            
            
            
            
                                # LEADERBOARD
                elif str(message.content.lower()) == "!gwins":
                    leaderboard = await Leaderboard.makeTextLB("gg wins")
                    await message.channel.send(embed = leaderboard)
                    
            
                elif str(message.content.lower()) == "!lb":
                    if (Leaderboard.makeLeaderboard("bread", breadLBPath) == True):
                        await message.channel.send(file=discord.File(breadLBPath))
                    else:
                        await message.channel.send("```\nLeaderboard is empty due to lack of players```")
            
            
            
                                
                                
                                # NICKNAMES
                elif message.content.startswith("!setname"):
                    await Utilities.setNickname(message)
                
                elif str(message.content.lower()) == "!name":
                    await Utilities.checkNickname(message)
        
        
        
        
            
                                # FLAG GAME
                elif str(message.content.lower()) == "!flaggame":
                    canBake, waitTime = Utilities.checkCooldown(message, "flaggame cooldown", 10)
                    if (canBake):
                        await FlagGame.startFlagGame(message, bot)
                    else:
                        if (int(waitTime) == 1):
                            body = "cooldown is " + waitTime + " minute"
                        else:
                            body = "cooldown is " + waitTime + " minutes"
                        embed = await Utilities.getEmbedMsg(body_text = body)
                        await message.channel.send(embed = embed)
            
            
            
            
            
                                # PROFILE
                elif (message.content.startswith("!profile") or message.content.startswith("!pf")):
                    await Utilities.showProfile(message, bot)
                
                
                
                
                
                #responds when a user @'s it
                elif "<@!416447447515267072>" in message.content:
                    body = f"```fix\nHi {message.author.name}!```"
                    footer = "type !help and I can show you around The Bakery!"
                    embed = await Utilities.getEmbedMsg(body_text = body, footer_text = footer)
                    await message.channel.send(embed = embed)
    
                    
                    
                    
                    
                
                
                                        # GUESSING GAME COMMANDS
                #start the guess game
                elif str(message.content).lower() == "start guessing":
                    await GuessingGame.startGuessGame(message)
                
                #read a user's guess
                elif str(message.author) != "The Baker#0723":
                    if (GuessingGame.checkIfGuessGameActive(message) != -1):
                        try:
                            number = int(message.content)
                        except:
                            pass
                        try:    
                            await GuessingGame.readGuess(message, number)
                        except:
                            pass
                    
            else:
                if (message.author.bot == True):
                    pass
                else:
                    await message.channel.send("you are not allowed in the bakery")




tokenPath = os.path.join("util/token.txt")
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
