import discord
from discord import client
from discord.ext import commands
from discord.ext.commands import has_permissions
from Setup import *
from Log import *
#If you are using this code create a file named edit config.txt  and insert your bot token

intents=intents=discord.Intents.all()



try:
    with open("Config.txt", "r")as file:
        Token = file.read().split(":")[1]
        print(Token)
except:
    print("Please insert your token in config.txt before starting the program")
    quit()


bot = commands.Bot(command_prefix="-", intents=intents)


#when bot joins server create data
@bot.event
async def on_guild_join(guild):
    serverId = guild.id
    if Serverexists(serverId):
        print("it exists")
    else:
        Setupserver(serverId, guild.owner_id)
    print(serverId)

#When Member joins the server add them to file
@bot.event
async def on_member_join(member):
    print(member.id)
    info = CheckMember(member.guild.id, member)
    print(info)
    if not info:
        Result = AddMember(member.guild.id, member.id)

    role = ServerGiveRank(member.guild.id)
    print(role)
    if not role == "NONE":
        roles = discord.utils.get(member.guild.roles, id=int(role))
        await member.add_roles(roles)
    location = ServerGetwelcome(member.guild.id)
    print(f"location{location}")
    if not location == "0":
        channel = bot.get_channel(int(location))
        await channel.send(f"Welcome to the server <@{member.id}>!!")

def LogChecker(guild):
    location = Logging(guild.id)
    if not location == "":
        return location
    else:
        return "null"

@bot.event
async def on_ready():
    bot.load_extension('Points')
    bot.load_extension('Messages')
    bot.load_extension('Moderation')
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

bot.run(Token)
