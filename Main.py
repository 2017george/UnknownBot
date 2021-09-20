import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from Setup import *

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

'''
Commands
 -Setup forces bot to reset the server infromation.
 -WelcomeChannel Makes a channel into a welcome channel
 '''

@bot.command(name="Setup")
#Resets the server data
async def Setup(ctx):
    print(ctx.message.author.id)
    if ctx.message.author.id == 318859316176355328:
        await on_guild_join(ctx.guild)
        await ctx.send(f"Completed setup")
    else:
        await ctx.send(f"Please message anunknown to use -setup")


@bot.command(name="WelcomeChannel")
@has_permissions(administrator=True)
async def WelcomeChannel(ctx, args="NONE"):
    if args == "NONE":
        await ctx.send(f"Please refrence a channel using  #id<@{ctx.message.author.id}>")
        return

    try:
        channel = bot.get_channel(int(args))
        AddServerWelcome(ctx.guild, args)
        await channel.send(f"Success <@{ctx.message.author.id}>")
    except:
        await ctx.send(f"The channel id that you have given is not a channgel please try again.! <@{ctx.message.author.id}>")


#setup main role that people get when they join the server.
@bot.command(name="mrole")
@has_permissions(manage_roles=True)
async def mrole(ctx, args="NONE"):
    if args == "NONE":
        await ctx.send(f"Please refrence a role by tagging the role <@{ctx.message.author.id}>")
        return

    Roles = await ctx.guild.fetch_roles()
    print(Roles, args)
    Roleid = args.replace("<@&", "").replace(">", "")
    print(Roleid)
    for i in Roles:
        if int(Roleid) == i.id:
            if AddServerRole(ctx.guild.id, Roleid):
                await ctx.send(f"<@&{Roleid}> has been set as the main role, and will be given to anyone who joins the server!")
            else:
                await ctx.send(f"Error please try again in 5 minutes!")
            break

#ban users
@bot.command(name="ban")
@has_permissions(ban_members=True)
async def ban(ctx, member : discord.Member, reason= None):
    await member.ban(reason = reason)
    await ctx.author.send(f"You have banned <@{member.id}> for {reason}")
    LoggingChannel = Logging(ctx.guild.id)
    if LoggingChannel == "":
        print("UMM")
        return
    else:
        channel = bot.get_channel(int(LoggingChannel))
        await channel.send(f"{ctx.author} has banned <@{member.id}> for {reason}")

#add logging channel
@bot.command(name="LoggingChannel")
@has_permissions(administrator=True)
async def LoggingChannel(ctx, args="NONE"):
    if args == "NONE":
        await ctx.send(f"Please refrence a channel using #id<@{ctx.message.author.id}>")
        return

    try:
        channel = bot.get_channel(int(args))
        AddLoggingChannel(ctx.guild.id, args)
        await channel.send(f"Success <@{ctx.message.author.id}>")
    except:
        await ctx.send(f"The channel id that you have given is not a channel please try again.! <@{ctx.message.author.id}>")


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
        print("adding")
        Result = AddMember(member.guild.id, member.id)
        print(f"Result{Result}")

    role = ServerGiveRank(member.guild.id)
    print(role)
    if not role == "NONE":
        roles = discord.utils.get(member.guild.roles, id=int(role))
        print(roles)
        await member.add_roles(roles)
    location = ServerGetwelcome(member.guild.id)
    print(f"location{location}")
    if not location == "0":
        channel = bot.get_channel(int(location))
        await channel.send(f"Welcome to the server <@{member.id}>")




@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
bot.run(Token)
