import discord
from discord.embeds import Embed
from discord.ext import commands
from discord.ext.commands import has_permissions


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
            await ctx.author.send(f"Please remember to add text at the end to the command for the bot to send! <@{ctx.message.author.id}>  \nThe following is the format that you need to have!\n Title|Color|Message...")
        else: 
            await splitMessage(ctx, message)

async def splitMessage(ctx, message):
    #try:
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
    #except: 
       # return False
def setup(bot):
    bot.add_cog(Messages(bot))