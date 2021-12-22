import discord, json


def Setupserver(guild, owner):
    with open(f"{guild}.json", "w+") as file:
        json.dump({"Roles":{},"Settings":{"JoinRank":"", "Welcome":"0", "logging":""},"Users":{owner:{}}}, file)
    return


def Serverexists(guild):
    try:
        with open(f"{guild}.json", "r")as file:
            if len(json.load(file)) > 0:
                return True
    except:
        return False


def CheckMember(guild, user):
    try:
        with open(f"{guild}.json", "r")as file:
            data = json.load(file)
            if not data['Users']['user'] == None:
                return True
            else:
                return False
    except:
        return False

def AddMember(guild, user):
     try:
        with open(f"{guild}.json", "r")as file:
            data = json.load(file)
            data['Users'][user] = {}
        with open(f"{guild}.json", "w")as file:
            json.dump(data, file)
     except:
         return False

def ServerGiveRank(guild):
    try:
        with open(f"{guild}.json", "r")as file:
            data = json.load(file)
            if not data['Settings']["JoinRank"] == "":
                return data['Settings']["JoinRank"]
            else:
                return "NONE"
    except:
        return "NONE"

def ServerGetwelcome(guild):
    try:
        with open(f"{guild}.json", "r")as file:
            data = json.load(file)
            if not data['Settings']["Welcome"] == "0":
                return data['Settings']["Welcome"]
            else:
                return "0"
    except:
        return "0"

def AddServerWelcome(guild, channel):
    try:
        with open(f"{guild}.json", "r")as file:
            data = json.load(file)
            data['Settings']["Welcome"] = str(channel)
        with open(f"{guild}.json", "w")as file:
            json.dump(data, file)

    except:
        return False

def AddServerRole(guild, role):
    try:
        with open(f"{guild}.json", "r")as file:
            data = json.load(file)
            data['Settings']["JoinRank"] = str(role)
            print(data)
        with open(f"{guild}.json", "w")as file:
            json.dump(data, file)
        return True
    except:
        return False

def Logging(guild):
    with open(f"{guild}.json", "r") as file:
        data = json.load(file)
        return data['Settings']["logging"]

def AddLoggingChannel(guild, channle):
    #try:
        with open(f"{guild}.json", "r")as file:
            data = json.load(file)
            data['Settings']["logging"] = str(channle)
            print(data)
        with open(f"{guild}.json", "w")as file:
            json.dump(data, file)
        return True
    # except:
    #     return False
