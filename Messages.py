import discord
from discord import embeds
from discord import colour
from discord.embeds import Embed
from discord.ext import commands
from discord.utils import get
from discord.ext.commands import has_permissions
from FileAccess import *


class Messages(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    #Message command sends a message in a specified area
    @commands.command(name = "Message")
    @has_permissions(administrator = True)
    async def Message(self, ctx, *, message= "None"):
        await ctx.message.delete()
        if message == "None": 
         await ctx.author.send(f"Please remember to add text at the end to the command for the bot to send! <@{ctx.message.author.id}>")
        else: 
         await ctx.send(f"{message}")
    #Embeded Messages
    @commands.command(name = "EMessage")
    @has_permissions(administrator = True)
    async def EMessage(self, ctx, *, message= "None"): 
        await ctx.message.delete()
        if message == "None": 
            await ctx.author.send(f"Please remember to add text at the end of the command for the bot to send! <@{ctx.message.author.id}>  \nThe following is the format that you need to have!\n Title|Color|Message or Title|Message")
        else: 
            if await splitMessage(ctx, message) == False: 
                ctx.author.send(f"Please follow the following format: \n Title|color|Message or Title|Message")
    @commands.command(name = "RMessage")
    @has_permissions(administrator = True)
    async def RMessage(self, ctx, *, message = "None"): 
        await ctx.message.delete()
        if message == "None": 
            await ctx.author.send(f"Please remeber to add the text at the end of the command for the bot to send! <@{ctx.message.author.id}> \nThe following is the format Message|Emoji = @role, Emoji2 = @role2")
        else: 
            await RoleMessage(ctx, message)
    @commands.command(name = "REMessage")
    @has_permissions(administrator = True)
    async def REMessage(self, ctx, *, message = "None"): 
        await ctx.message.delete()
        if message == "None": 
            await ctx.author.send(f"Please remeber to add the text at the end of the command for the bot to send! <@{ctx.message.author.id}> \nThe following is the format Message|Emoji = @role, Emoji2 = @role2")
        else: 
            await RoleEMessage(ctx, message)


#listens for anything to do with reactions
class ReactionListener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #Listener for when the user adds a reaction    
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, reaction):
        #get from json file all the data about any possible reaction messages
        MessageExists = FindMessage(reaction.guild_id, reaction.message_id) 
        #if there are non with the message id esc the function
        if MessageExists == "False": 
            return
        else:
            #set a final role to nothing 
            FinalRole  = "None"
            #go through all the possible roles to be given
            for i in(MessageExists):
                emojiRole = i.split(":")
                #check if the emoji is a normal emoji
                if(reaction.emoji.name) == i[0].replace(' ', ""):
                    FinalRole = emojiRole[1]
                #check if the emoji is a custom emoji
                elif(reaction.emoji.name.isalpha()):
                    if(reaction.emoji.name == i.replace('<:', '').split(":")[0]):
                        FinalRole = emojiRole[3]
            
            #check if a role has been found
            if(FinalRole == "None"): 
               await reaction.member.send("An error has occured please try again later!")
            #give the role to the user who has selected it
            else: 
                guild = self.bot.get_guild(reaction.guild_id)
                for i in  await guild.fetch_roles():
                    if(int(FinalRole.replace(">", "")) == i.id): 
                        await reaction.member.add_roles(i)


    #Listener for when the user un reacts
    @commands.Cog.listener() 
    async def on_raw_reaction_remove(self, reaction): 
        #get from json file all the data about any possible reaction messages
        MessageExists = FindMessage(reaction.guild_id, reaction.message_id) 
        #if there are non with the message id esc the function
        if MessageExists == "False": 
            return
        else:
            #set a final role to nothing 
            FinalRole  = "None"
            #go through all the possible roles to be given
            for i in(MessageExists):
                emojiRole = i.split(":")
                #check if the emoji is a normal emoji
                if(reaction.emoji.name) == i[0].replace(' ', ""):
                    FinalRole = emojiRole[1]
                #check if the emoji is a custom emoji
                elif(reaction.emoji.name.isalpha()):
                    if(reaction.emoji.name == i.replace('<:', '').split(":")[0]):
                        FinalRole = emojiRole[3]
            
            #check if a role has been found
            if(FinalRole == "None"): 
               await reaction.member.send("An error has occured please try again later!")
            #give the role to the user who has selected it
            else: 
                
                guild = self.bot.get_guild(reaction.guild_id)
                member = get(guild.members, id=reaction.user_id)
                for i in  await guild.fetch_roles():
                    if(int(FinalRole.replace(">", "")) == i.id): 
                        if i in member.roles:
                            await member.remove_roles(i)

        
async def RoleEMessage(ctx, message):
    #try:
        x = message.split("|")
        if(len(x) == 3): 
            
            #await ctx.send(embed = em)
            FMessage = f"{x[1]} \n"
            #allow for multiple roles to be given out per message or a single role per message
            try:
                roles = x[2].split(",")
            except: 
                roles = [x[2]]
            print(roles)
            #Gets all the roles from the server
            ServerRoles = await ctx.guild.fetch_roles()
            emojis = []
            FinalReactionEmoji = ""
            #Checks if each of the roles that are in the message exists in the server
            for i in roles: 
                role = i.split("=")[1].replace(" ", "").replace("<@&", "").replace(">", "")
                exists = False
                print(role)
                for x in ServerRoles: 
                    if(int(role)==x.id):
                        exists = True
                        FMessage += f"{i.split('=')[0]} = {i.split('=')[1]}\n"
                if exists == False: 
                    #one of the roles do not exist
                    await ctx.author.send("One of the Roles you have indecated does not exist please check it and try again!")
                    break
                else: 
                    #adds the roles to be sent in the final message
                    
                    emojis.append(i.split('=')[0].replace(" ", ""))
                    FinalReactionEmoji += f"{i.split('=')[0].replace(' ', '')}:{role},"
            FinalReactionEmoji = FinalReactionEmoji[:-1:]
            #if there where no errors it sends the message and adds reactions 
            if exists == True: 
                print(x)
                em = discord.Embed(title = x, description = FMessage, colour = discord.Color.random())
                MessageId = await ctx.send(embed = em)
                for i in emojis:
                    await MessageId.add_reaction(i)
                #sends this new message with reactions roles into the server file
                MessageReaction(ctx.guild.id, MessageId.id, FinalReactionEmoji)
                

        elif(len(x) == 4): 
            print(x)
            title = x[0]
            color = x[1]
            FMessage = f"{x[2]} \n"
            #allow for multiple roles to be given out per message or a single role per message
            try:
                roles = x[3].split(",")
            except: 
                roles = [x[3]]
            print(roles)
            #Gets all the roles from the server
            ServerRoles = await ctx.guild.fetch_roles()
            emojis = []
            FinalReactionEmoji = ""
            #Checks if each of the roles that are in the message exists in the server
            for i in roles: 
                role = i.split("=")[1].replace(" ", "").replace("<@&", "").replace(">", "")
                exists = False
                print(role)
                for x in ServerRoles: 
                    if(int(role)==x.id):
                        exists = True
                        FMessage += f"{i.split('=')[0]} = {i.split('=')[1]}\n"
                if exists == False: 
                    #one of the roles do not exist
                    await ctx.author.send("One of the Roles you have indecated does not exist please check it and try again!")
                    break
                else: 
                    #adds the roles to be sent in the final message
                    
                    emojis.append(i.split('=')[0].replace(" ", ""))
                    FinalReactionEmoji += f"{i.split('=')[0].replace(' ', '')}:{role},"
            FinalReactionEmoji = FinalReactionEmoji[:-1:]
            #if there where no errors it sends the message and adds reactions 
            if exists == True: 
                print(x)
                if(color.lower() == "blue"):
                    em = discord.Embed(title = title, description = FMessage, colour = discord.Color.blue())

                elif(color.lower() == "purple"):
                    em = discord.Embed(title = title, description = FMessage, colour = discord.Color.purple())

                elif(color.lower() == "red"):
                    em = discord.Embed(title = title, description = FMessage, colour = discord.Color.red())

                elif(color.lower() == "orange"):
                    em = discord.Embed(title = title, description = FMessage, colour = discord.Color.orange())
                elif(color.lower() == "black"):
                    em = discord.Embed(title = title, description = FMessage, colour = discord.Color.darker_grey())
                MessageId = await ctx.send(embed = em)
                for i in emojis:
                    await MessageId.add_reaction(i)
                #sends this new message with reactions roles into the server file
                MessageReaction(ctx.guild.id, MessageId.id, FinalReactionEmoji)
        else: 
            return False
    #except: 
      # return False
async def RoleMessage(ctx, message): 
    '''
    Format
    Message|Emoji = Role

    '''
    #try: 
    #seperate the values 
    x = message.split("|")
    if(len(x) == 2): 
        FMessage = f"{x[0]} \n"
        #allow for multiple roles to be given out per message or a single role per message
        try:
            roles = x[1].split(",")
        except: 
            roles = [x[1]]
        #Gets all the roles from the server
        ServerRoles = await ctx.guild.fetch_roles()
        emojis = []
        FinalReactionEmoji = ""
        #Checks if each of the roles that are in the message exists in the server
        for i in roles: 
            role = i.split("=")[1].replace(" ", "").replace("<@&", "").replace(">", "")
            exists = False
            for x in ServerRoles: 
                if(int(role)==x.id):
                    exists = True
            if exists == False: 
                #one of the roles do not exist
                await ctx.author.send("One of the Roles you have indecated does not exist please check it and try again!")
                break
            else: 
                #adds the roles to be sent in the final message
                FMessage += f"{i.split('=')[0]} = {i.split('=')[1]}\n"
                emojis.append(i.split('=')[0].replace(" ", ""))
                FinalReactionEmoji += f"{i.split('=')[0].replace(' ', '')}:{role},"
        FinalReactionEmoji = FinalReactionEmoji[:-1:]
        #if there where no errors it sends the message and adds reactions 
        if exists == True: 
            MessageId = await ctx.send(FMessage)
            for i in emojis:
                await MessageId.add_reaction(i)
            #sends this new message with reactions roles into the server file
            MessageReaction(ctx.guild.id, MessageId.id, FinalReactionEmoji)
            
            
    #except: 
        #return False
async def splitMessage(ctx, message):
    try:
        x = message.split("|")
        if(len(x) == 2): 
            em = discord.Embed(title = x[0], description = x[1], colour = discord.Color.random())
            await ctx.send(embed = em)

        elif(len(x) == 3): 
            if(x[1].lower() == "blue"):
                em = discord.Embed(title = x[0], description = x[2], colour = discord.Color.blue())
                await ctx.send(embed = em)
            elif(x[1].lower() == "purple"):
                em = discord.Embed(title = x[0], description = x[2], colour = discord.Color.purple())
                await ctx.send(embed = em)
            elif(x[1].lower() == "red"):
                em = discord.Embed(title = x[0], description = x[2], colour = discord.Color.red())
                await ctx.send(embed = em)
            elif(x[1].lower() == "orange"):
                em = discord.Embed(title = x[0], description = x[2], colour = discord.Color.orange())
                await ctx.send(embed = em)
            elif(x[1].lower() == "black"):
                em = discord.Embed(title = x[0], description = x[2], colour = discord.Color.darker_grey())
                await ctx.send(embed = em)
        elif(len(x) == 1):
            em = discord.Embed(description = x[0], colour = discord.Color.random())
            await ctx.send(embed = em)
        else: 
            return False
    except: 
       return False
def setup(bot):
    bot.add_cog(Messages(bot))
    bot.add_cog(ReactionListener(bot))