import discord

async def JoinLog(bot, location, member):
    channel = bot.get_channel(int(location))
    await channel.send(f"Welcome to the server <@{member.id}>")