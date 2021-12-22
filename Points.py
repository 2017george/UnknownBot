from datetime import date
import discord, random, json
from discord import embeds
from discord import colour
from discord import user
from discord import mentions
from discord.embeds import Embed
from discord.ext import commands
from discord.utils import get
from discord.ext.commands import has_permissions

class Points(commands.Cog): 
    def __init__(self, bot): 
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, message): 
        if(not message.author.bot):
            points = random.randint(1,3)
            AddPoints(message.guild.id, message.author.id, points)

    @commands.command(name="GivePoints")
    @has_permissions(administrator = True)
    async def GivePoints(self, ctx, member: discord.Member, points):
        await ctx.message.delete()
        try: 
            points = int(points)
            AddPoints(ctx.guild.id, member.id, points)
            await ctx.send(f"Success <@{ctx.author.id}>, {member.name} has gained {points}")
        except: 
           await ctx.author.send("Please only put a the number of points you would like to give the member!\n Use this format -GivePoints @ member points")
    @commands.command(name="LevelList")
    async def LevelList(self, ctx): 
        await ctx.message.delete()
        EPoints = Top5(ctx.guild.id)
        em = discord.Embed(title = "Top 5 people with most points!")
        Users = ""
        Point = ""
        Place = ""
        for i in range(5):
            try:
                Users += get(self.bot.get_all_members(), id=int(EPoints[i][1])).name + "\n"
                Point += str(EPoints[i][0]) + "\n"
                Place += str(i+1) + "\n"
            except: 
                pass
        em.add_field(name = "#", value=Place, inline=True)
        em.add_field(name = "Names", value=Users, inline=True) 
        em.add_field(name = "Points", value=Point, inline=True)
        em.set_footer(text= f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed = em)
        pass
    @commands.command(name="Level")
    async def Level(self, ctx): 
        await ctx.message.delete()
        points = GetPoints(ctx.guild.id, ctx.author.id)
        if points == None: 
            await ctx.author.send(f"An Error has occured with your account please type something in chat and try ruinning the command again!")
        else: 
            em = discord.Embed(description= f"You have **{points} UBucks!** ")
            em.set_author(name=f"{ctx.author.name}'s Points", icon_url=ctx.author.avatar_url)
            em.set_footer(text= "You can gain more UBucks by talking in chat!")
            await ctx.send(embed= em)


def GetPoints(guild, authorId): 
    with open(f"{guild}.json", "r") as file: 
        data = json.load(file)
        try:
            return data["Users"][str(authorId)]["Points"]
        except: 
            return None

def AddPoints(guild, authorId, points): 
    with open(f"{guild}.json", "r") as file: 
        data = json.load(file)
        try: 
            points += int(data["Users"][str(authorId)]["Points"])
            if(points < 0): 
                points = 0
            data["Users"][str(authorId)]["Points"] = points
        except: 
            if(points < 0): 
                points = 0
            try:
                data["Users"][str(authorId)]["Points"] = points
            except:
                data["Users"][str(authorId)] = {"Points": points}
    with open(f"{guild}.json", "w") as file: 
        json.dump(data, file)

def Top5(guild):
    with open(f"{guild}.json", "r") as file: 
        data = json.load(file)
        Epoints = []
        for i in data["Users"]: 
            try:
                points = data["Users"][i]["Points"]
                Epoints.append([points, i])
            except: 
                pass
        Epoints.sort(reverse = True)
        return Epoints


def setup(bot): 
    bot.add_cog(Points(bot))