from discord import *

#If you are using this code create a file named edit config.txt  and insert your bot token

try:
    with open("Config.txt", "r")as file:
        Token = file.read().split(":")[1]
except:
    Print("Please insert your token in config.txt before starting the program")
    quit()
