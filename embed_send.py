import discord

class send_embed():
    def __init__(self, message, user):
        self.message = message
        self.user = user

    async def send(self, title, send_message, image, types='png'):
        message = self.message
        user = self.user
        self.types = types
        self.image = image
        sending = discord.Embed(Title = 'this is a test', colour = discord.Colour.blue())
        img = discord.File(image, filename="image."+types)
        sending.add_field(name = title, value =send_message.format(message) ,inline=False)
        sending.set_image(url='attachment://image.'+types)
        msg = await message.channel.send(file=img , embed=sending )
        self.img = img
        self.msg = msg
        return msg
    async def send_no(self, title, send_message, color =discord.Colour.blue()):
        message = self.message
        user = self.user
        sending = discord.Embed(Title = 'this is a test', colour = color)
        sending.add_field(name = title, value =send_message.format(message) ,inline=False)
        msg = await message.channel.send(embed=sending )
        self.msg = msg
        return msg
    async def send_file(self, title, send_message, location):
        message = self.message
        user = self.user
        txt = discord.File(location)
        sending = discord.Embed(Title = 'this is a test', colour = discord.Colour.blue())
        sending.add_field(name = title, value =send_message.format(message) ,inline=False)
        msg = await message.channel.send(embed=sending)
        await message.channel.send(file=txt) 
        self.msg = msg
        return msg
    async def edit(self, send_message, title):
        message = self.message
        msg = self.msg
        user = self.user
        image = self.image
        types = self.types
        img = discord.File(image, filename="image."+types)
        sending = discord.Embed(Title = 'this is a test', colour = discord.Colour.blue())
        sending.set_image(url='attachment://image.'+types)
        sending.add_field(name = title, value = send_message.format(message) ,inline=False)

        await msg.edit(embed = sending )
