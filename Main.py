import discord
from discord.ext import commands
from Setup import *

#If you are using this code create a file named edit config.txt  and insert your bot token

try:
    with open("Config.txt", "r")as file:
        Token = file.read().split(":")[1]
        print(Token)
except:
    Print("Please insert your token in config.txt before starting the program")
    quit()


bot = commands.Bot(command_prefix="-")
@bot.command(name="Help")
async def Help(ctx, arg):
    await ctx.send(f"I see you have passed {len(arg)} arguments, {arg}")

@bot.command(name="Setup")
async def Setup(ctx):
    print(ctx.message.author.id)
    if ctx.message.author.id == 318859316176355328:
        await on_guild_join(ctx.guild)
        await ctx.send(f"Completed setup")
    else:
        await ctx.send(f"Please message anunknown to use -setup")

@bot.event
async def on_guild_join(guild):
    serverId = guild.id
    if Serverexists(serverId):
        print("it exists")
    else:
        Setupserver(serverId, guild.owner_id)
    print(serverId)


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
bot.run(Token)
