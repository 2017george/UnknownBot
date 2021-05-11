import discord
from embed_send import *
from Drop import *

Token = 'ODQxNTA0NzkwOTE5MzgxMDAz.YJnuaA.v9zJidTc4H4t8dwK6WlP1KTgR4I'
#https://discordapp.com/oauth2/authorize?client_id=841504790919381003&scope=bot

client = discord.Client()
sign = "-"

@client.event
async def on_message(message):
    send = send_embed(message, message.author)
    if message.content == sign+"dropadd":
        if message.attachments == []:
            await send.send_no("Missing File", "You are Missing the file please insert file and try again!", color=discord.Colour.red())
        else:
            file_names = []
            for i in message.attachments:
                try:
                    if i.filename.split(".")[1] == "txt":
                        await i.save(i.filename)
                        file_names.append(i.filename)
                    else:
                        await send.send_no("File Error", "File Error! \nThe file you provided has an error. \nIf the file provided is not a .txt file please change it\nOtherwise message CuziamUnknown!", color=discord.Colour.red())
                except:
                    await send.send_no("File Error", "File Error! \nThe file you provided has an error. \nIf the file provided is not a .txt file please change it\nOtherwise message CuziamUnknown!", color=discord.Colour.red())
            Final = Dropadd(file_names)

    elif message.content == (sign+"drop"):
        if message.attachments == []:
            await send.send_no("Missing File", "You are Missing the file please insert file and try again!", color=discord.Colour.red())
        else:
            file_names = []
            for i in message.attachments:
                try:
                    if i.filename.split(".")[1] == "txt":
                        await i.save(i.filename)
                        file_names.append(i.filename)
                    else:
                        await send.send_no("File Error", "File Error! \nThe file you provided has an error. \nIf the file provided is not a .txt file please change it\nOtherwise message CuziamUnknown!", color=discord.Colour.red())
                except:
                    await send.send_no("File Error", "File Error! \nThe file you provided has an error. \nIf the file provided is not a .txt file please change it\nOtherwise message CuziamUnknown!", color=discord.Colour.red())
            Final = Drop(file_names)
    elif message.content == (sign+"output"):
        with open("output.txt", "r")as o:
            if o.read() == "":
                await send.send_no("File Error", "File Error! \nThe file you provided has an error. \nNo files where uploded please upload a txt file using -drop or -dropadd\nOtherwise message CuziamUnknown!", color=discord.Colour.red())
            else:
                await send.send_file("Output", "The final output is:", "Output.txt")
                with open("output.txt", "w")as o:
                    o.write("")
    elif message.content == (sign+"help"):
        await send.send_no("Help", "Hello, I am UnknownBot\nI am here to help make your lives easier.\n\nHere are a few of the things I do:\n\n1.Convert drop logs to item return logs:\n   -drop with a file starts a new drop file.\n -dropadd adds to an existing file. \n -output is to export the final file!\n\n2.MY Dev Is working :D")







@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(Token)
