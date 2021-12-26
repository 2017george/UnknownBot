from datetime import date
import discord, random, json, os
from discord import message
from discord.ui import Button, View, view
from discord.embeds import Embed
from discord.ext import commands, tasks
from discord.utils import get
from discord.ext.commands import has_permissions

class CharCards(commands.Cog) :
    def __init__(self, bot): 
        self.bot = bot
        self.LoadChar()
        self.NewCard.start()
    
    def LoadChar(self): 
        # assign directory
        self.characters = []
        directory = f'{os.getcwd()}/Characters'

        for filename in os.scandir(directory):
            if filename.is_file():
                self.characters.append(filename.name)

    @commands.command(name="CCSetup")
    @has_permissions(administrator= True)
    async def CCSetup(self, ctx, args = None): 
        await ctx.message.delete()
        if args == None: 
            SelectChannel(ctx.guild.id, ctx.channel)
            await ctx.author.send(f"Success the Character cards channel is {ctx.channel.name}")
        else: 
            try:
                channel = self.bot.get_channel(int(args))
                SelectChannel(ctx.guild.id, args)
                await ctx.author.send(f"Success the Character cards channel is {channel.name}")
            except:
                await ctx.author.send(f"The channel id that you have given is not a channgel please try again.! <@{ctx.message.author.id}>")
    @tasks.loop(minutes = 30)
    #@tasks.loop(seconds=2)
    async def NewCard(self): 
        guilds =  self.bot.guilds
        for i in guilds: 
            try:
                args = GetChannel(i.id)
                channel = self.bot.get_channel(int(args))
                await self.WinningBid(i, channel)
                await self.SendCard(channel, i.id)

            except: 
                pass
    async def SendCard(self, channel, guild): 
        #Sends the message of the card based off of it getting a random number
        x = random.randint(0,len(self.characters)-1)
        price = int(self.characters[x].split('|')[1].split(".")[0])
        finalPrice = price * random.randint(2,20)

        #Gets the image and stores it into a discord.file
        file = discord.File(f"{os.getcwd()}/Characters/{self.characters[x]}", filename="image.png")
        
        #creates the embed
        em = discord.Embed(title= f"{self.characters[x].split('|')[0]} has appeared!")
        em.set_image(url=f"attachment://image.png")
        em.set_footer(text=f"{self.characters[x].split('|')[0]} can be purchaced for {finalPrice} UBucks\nOr you may auction for it current auction is {price} UBucks!")
        #sends the message and stores message detail in json file
        Message = await channel.send(file = file, embed=em)
        SelectedMessage(guild, Message.id, self.characters[x], price, finalPrice)
        
        #Setup buy +bid + 100 bid buttons
        buy = Button(label=f"Buy U{finalPrice}", style=discord.ButtonStyle.primary)
        plusT = Button(label=f"Bid +U10", style=discord.ButtonStyle.primary, custom_id="10")
        plusH = Button(label=f"Bid +U100", style=discord.ButtonStyle.primary,custom_id="100")
        plusTH = Button(label=f"Bid +U1000", style=discord.ButtonStyle.primary, custom_id="1000")

        #config each button to call a function
        buy.callback = Buy
        plusT.callback = Bid
        plusH.callback = Bid
        plusTH.callback = Bid

        v = View()
        v.add_item(buy)
        v.add_item(plusT)
        v.add_item(plusH)
        v.add_item(plusTH)
        await Message.edit(view = v)

    async def WinningBid(self, guild, channel):
        try:
            x = GiveWinner(guild.id)
            user =(guild.get_member(int(x[4])))

            msg = await channel.fetch_message(int(x[0])) 
            em = msg.embeds[0]
            em.title = f"The Bid on {x[1].split('|')[0]} has ended"
            em.set_footer(text=f"{user.name} Has Won the bid on {x[1].split('|')[0]}",  icon_url=user.display_avatar)
            await msg.edit (embed = em, view = None)


        except:
            x = GetMessage(guild.id)
            if(x == 0): 
                return 0
            msg = await channel.fetch_message(int(x[0])) 
            em = msg.embeds[0]
            em.title = f"The Bid on {x[1].split('|')[0]} has ended"
            em.set_footer(text=f"No one has won {x[1].split('|')[0]}")
            await msg.edit (embed = em, view = None)
            return 0
    
    @commands.command(name = "CCards")
    async def CCards(self, ctx, page = 1): 
        await ctx.message.delete()
        guild = ctx.guild.id
        member = ctx.author.id
        x = GetCards(guild, member)
        if(x == 0): 
            await ctx.send(f"You don't have any cards <@{ctx.author.id}>!")
        else: 
            send = False
            em = discord.Embed(title=f"Your Cards Page {page}:")
            Message = ""
            for i in range(1*int(page), 10*int(page)):
                try: 
                    Message += f"**{i}: {x[i-1].split('|')[0]}**\n"
                    send = True
                except:
                    pass
            em.description= Message
            if(len(x)> 10 * int(page)):
                em.set_footer(text= f"To see more cards do -CCards {page+1}", icon_url=ctx.author.display_avatar.url)
            else:
                 em.set_footer(text= f"Cards belong to {ctx.author.name}", icon_url=ctx.author.display_avatar.url)

            if send:
                await ctx.send(embed = em)
            else: 
                await ctx.send(f"You don't have any cards <@{ctx.author.id}>!")
        pass


def GetCards(guild, id): 
    with open(f"{guild}.json", "r") as file: 
        data = json.load(file)
    try: 
        cards = data["Users"][str(id)]["CCards"]
        return cards
    except:
        return 0

def GiveWinner(guild):
    with open(f"{guild}.json", "r") as file: 
        data = json.load(file)
    
    try: 
        card = data["CharacterCard"][1]
        winner = data["CharacterCard"][4]
        price = data["CharacterCard"][2]
        points = data["Users"][str(winner)]["Points"]
        cards = data["Users"][str(winner)]["CCards"]
        cards.append(card)
        points = int(points) - int(price)
        data["Users"][str(winner)]["Points"] = points
        data["Users"][str(winner)]["CCards"] = cards
        with open(f"{guild}.json", "w") as file: 
            json.dump(data, file)
        return data["CharacterCard"]
    except:
        return 0

async def Bid(interaction):
    user = (interaction.user.id)
    guild = interaction.guild.id
    ammount =int(interaction.data["custom_id"])

    x = InsertBid(guild, user, ammount)
    if x == 0:
        await interaction.response.send_message("You dont have enough points!\nCheck you points by doing -Level", ephemeral = True)
    elif x == 1: 
        await interaction.response.send_message("You already own this card!\nCheck your cards by doing -CCards", ephemeral = True)
    else: 
        await interaction.response.send_message(f"You now have the higest bid on {x[1].split('|')[0]}", ephemeral = True)
        

        em = interaction.message.embeds[0]
        em.set_footer(text=f"{x[1].split('|')[0]} can be purchaced for {x[3]} UBucks\nThe Highest bid is by: {interaction.user.name} for {x[2]} UBucks",  icon_url=interaction.user.display_avatar)
        await interaction.followup.edit_message(message_id = interaction.message.id , embed = em)

def GetMessage(guild): 
    with open(f"{guild}.json", "r") as file: 
        data = json.load(file)
    try:
        x = data["CharacterCard"]
        return x 
    except:
        return 0

def InsertBid(guild, user, ammount): 
    with open(f"{guild}.json", "r") as file: 
        data = json.load(file)
    try: 
        Possible = False
        own = False
        Avalible_points = data["Users"][str(user)]["Points"]
        Current = data["CharacterCard"]
        owns = []
        try:
            owns = data["Users"][str(user)]["CCards"]
            for i in owns:
                if(i == Current[1]): 
                    own = True
                    return 1
        except: 
            pass
       
        if int(Avalible_points) >= int(Current[2])+ammount: 
            data["CharacterCard"][4] = user
            data["CharacterCard"][2] = (int(Current[2]) + ammount)
            with open(f"{guild}.json", "w") as file: 
                json.dump(data, file)
            return data["CharacterCard"]
        else: 
            return 0 
    except:
        return 0

async def Buy(interaction): 
    user = (interaction.user.id)
    guild = interaction.guild.id
    x = Purchase(guild, user)
    if x == 0:
        await interaction.response.send_message("You dont have enough points!\nCheck you points by doing -Level", ephemeral = True)
    elif x == 1: 
        await interaction.response.send_message("You already own this card!\nCheck your cards by doing -CCards", ephemeral = True)
    else: 
        await interaction.response.send_message(f"Congrats you now own {x[1].split('|')[0]}", ephemeral = True)
        
        em = interaction.message.embeds[0]
        em.title=f"{x[1].split('|')[0]} Has been purchased"
        em.set_footer(text=f"{x[1].split('|')[0]} has been purchased by {interaction.user.name}", icon_url=interaction.user.display_avatar)
        await interaction.followup.edit_message(message_id = interaction.message.id , embed = em, view = None)


def Purchase(guild, user): 
    with open(f"{guild}.json", "r") as file: 
        data = json.load(file)
    try: 
        Possible = False
        own = False
        Avalible_points = data["Users"][str(user)]["Points"]
        Current = data["CharacterCard"]
        owns = []
        try:
            owns = data["Users"][str(user)]["CCards"]
            for i in owns:
                if(i == Current[1]): 
                    own = True
                    return 1
        except: 
            pass
       
        if int(Avalible_points) >= int(Current[3]): 
            Avalible_points = int(Avalible_points) - int(Current[3])
            owns.append(Current[1])
            data["Users"][str(user)]["Points"] = Avalible_points
            data["Users"][str(user)]["CCards"]= owns
            x = data["CharacterCard"]
            data["CharacterCard"] = []
            with open(f"{guild}.json", "w") as file: 
                json.dump(data, file)
            return x
        else: 
            return 0 
    except:
        return 0
    


def SelectChannel(guild, channel): 
    with open(f"{guild}.json", "r") as file: 
        data = json.load(file)
    try: 
        data["Settings"]["CharCards"] = str(channel)
    except: 
        pass
    with open(f"{guild}.json", "w") as file: 
        json.dump(data, file)

def GetChannel(guild):
    with open(f"{guild}.json", "r") as file: 
        data = json.load(file)
    try: 
        return data["Settings"]["CharCards"]
    except: 
        return None

def SelectedMessage(guild, MessageId, Card, price, FinalPrice):
    with open(f"{guild}.json", "r") as file: 
        data = json.load(file)
    try: 
        data["CharacterCard"] = [MessageId, Card, price, FinalPrice, ""]
    except: 
        pass
    with open(f"{guild}.json", "w") as file: 
        json.dump(data, file)

    
def setup(bot): 
    bot.add_cog(CharCards(bot))