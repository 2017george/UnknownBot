import discord, json


def Setupserver(guild, owner):
    with open(f"{guild}.json", "w+") as file:
        json.dump({"Roles":{},"Settings":{},"Users":{owner:{}}}, file)
    return


def Serverexists(guild):
    try:
        with open(f"{guild}.json", "r")as file:
            if len(json.load(file)) > 0:
                return True
    except:
        return False
