import discord, json

def MessageReaction(guild, messageid, Reactions): 
    '''
    Reactions format
    Emoji:RoleId,Emoji:RoleId
    Send to Json 
    "messageid":{Emoji:RoleID,Emoji:RoleID}
    '''
    ReactionsList = []
    try:
        Reactions= Reactions.split(",")
        for i in range(len(Reactions)):
            ReactionsList.append(Reactions[i])
    except: 
        ReactionsList.append(Reactions)
        pass
    
    newData = {messageid:ReactionsList}
    with open(f"{guild}.json", "r")as file:
        data = json.load(file)
    with open(f"{guild}.json", "w")as file:
        data.update(newData)
        json.dump(data, file, ensure_ascii=False)
    pass


def FindMessage(guild, MessageID): 
    try: 
        with open(f"{guild}.json", "r") as file: 
            data = json.load(file)
            if not data[str(MessageID)] == None: 
                return data[str(MessageID)]
            else: 
                return "False"
    except: 
        return "False"
