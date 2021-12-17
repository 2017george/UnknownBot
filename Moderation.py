import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from Setup import *
from Log import *

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    #Server setup systems
    #add logging channel
    @commands.command(name="LoggingChannel")
    @has_permissions(administrator=True)
    async def LoggingChannel(self, ctx, args="NONE"):
        await ctx.message.delete()
        if args == "NONE":
            await ctx.send(f"Please refrence a channel using #id<@{ctx.message.author.id}>")
            return

        try:
            channel = self.bot.get_channel(int(args))
            AddLoggingChannel(ctx.guild.id, args)
            await channel.send(f"Success <@{ctx.message.author.id}>")
        except:
            await ctx.send(f"The channel id that you have given is not a channel please try again.! <@{ctx.message.author.id}>")

    @commands.command(name="Setup")
    #Resets the server data
    async def Setup(self, ctx):
        await ctx.message.delete()
        print(ctx.message.author.id)
        if ctx.message.author.id == 318859316176355328:
            await self.bot.on_guild_join(ctx.guild)
            await ctx.send(f"Completed setup")
        else:
            await ctx.send(f"Please message anunknown to use -setup")
   
   #Setup a Wellcome message channel where anytime somone joins it welcomes them
    @commands.command(name="WelcomeChannel")
    @has_permissions(administrator=True)
    async def WelcomeChannel(self, ctx, args="NONE"):
        await ctx.message.delete()
        if args == "NONE":
            channel = ctx.channel
            print(channel)
            AddServerWelcome(ctx.guild.id, channel.id)
            await channel.send(f"Success <@{ctx.message.author.id}>")
        else:
            try:
                channel = self.bot.get_channel(int(args))
                AddServerWelcome(ctx.guild.id, args)
                await channel.send(f"Success <@{ctx.message.author.id}>")
            except:
                await ctx.send(f"The channel id that you have given is not a channgel please try again.! <@{ctx.message.author.id}>")


    #setup main role that people get when they join the server.
    @commands.command(name="mrole")
    @has_permissions(manage_roles=True)
    async def mrole(self, ctx, args="NONE"):
        await ctx.message.delete()
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

    '''
    Moderating the server commands
    Ban = bans the user from the server (reqires ban access)
    Kick = kicks the user from the server (requires kick permision)
    '''
    #ban users
    @commands.command(name="ban")
    @has_permissions(ban_members=True)
    async def ban(self, ctx, member : discord.Member, *, Reason= None):
        await ctx.message.delete()
        await member.ban(reason = Reason)
        if Reason == None:
            await ctx.author.send(f"You have banned <@{member.id}>!")
        else:
            await ctx.author.send(f"You have banned <@{member.id}> for {Reason}!")
        LoggingChannel = Logging(ctx.guild.id)
        print(LoggingChannel)
        if LoggingChannel == "":
            print("UMM")
            return
        else:
            channel = self.bot.get_channel(int(LoggingChannel))
            await channel.send(f"{ctx.author} has banned <@{member.id}> for {Reason}!")

    #kick users
    @commands.command(name="kick")
    @has_permissions(kick_members = True)
    async def kick(self, ctx, member: discord.Member, *, Reason = None):
        await ctx.message.delete()
        await member.kick(reason= Reason)
        if Reason == None: 
            await ctx.author.send(f"You Kicked <@{member.id}>!")
        else: 
            await ctx.author.send(f"You Kicked <@{member.id}> for {Reason}!")
        LoggingChannel = Logging(ctx.guild.id)
        if LoggingChannel == "":
            print("UMM")
            return
        else:
            channel = self.bot.get_channel(int(LoggingChannel))
            await channel.send(f"{ctx.author} has kicked <@{member.id}> for {Reason}!")


def setup(bot):
    bot.add_cog(Moderation(bot))