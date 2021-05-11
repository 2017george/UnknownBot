import os
def Drop(files):
    logs = ""
    for i in files:
        with open(i, "r") as log:
            logs += log.read()
        logs += "},"
    Items = {}
    logs = logs.split("},")
    for i in logs:
        if "{" in i and "}" in i:
            item = i.split("{")
            for it in item:
                item_name = it.split("}")[0]
                if "[" in it :

                     try:
                        if "|| ||" in it:
                          n  = it.split("[")[1]
                          n = n.split("|| ||")[0]
                        else:
                          n  = it.split("[")[2]


                        enchant = n.split("]")[0]
                        if not enchant in item_name:
                            item_name += ", ["+ enchant +"]"


                     except:
                        pass


        else:

            item = i.split("{")
            for it in item:
                item_name = it.split(":")[0]
        x = i.split(" ")
        for z in x:
            if "x" in z:
                try:
                    nums = z.replace(",", "")
                    num = int(nums.replace("x", ""))
                    if item_name in Items:
                        i_num = Items[item_name] + num
                        Items[item_name] = i_num
                    else:
                        Items[item_name] = num
                except:
                    pass
    with open("Output.txt", "w+") as output:
        final = ""
        for i in Items:
            final += (str(Items[i])+ "x "+ i+"\n")
        output.write(final)
    for i in files:
        os.remove(i)


def Dropadd(files):
    logs = ""
    for i in files:
        with open(i, "r") as log:
            logs += log.read()
        logs += "},"
    Items = {}
    with open("Output.txt", "r") as output:
        old = output.read()
    for i in old.split("\n"):
        try:
            Items[i.split("x ")[1].replace("\'","")] = int(i.split("x ")[0])
        except:
            pass
        #
    logs = logs.split("},")
    for i in logs:
        if "{" in i and "}" in i:
            item = i.split("{")
            for it in item:
                item_name = it.split("}")[0]
                if "[" in it :

                     try:
                        if "|| ||" in it:
                          n  = it.split("[")[1]
                          n = n.split("|| ||")[0]
                        else:
                          n  = it.split("[")[2]


                        enchant = n.split("]")[0]
                        if not enchant in item_name:
                            item_name += ", ["+ enchant +"]"


                     except:
                        pass


        else:

            item = i.split("{")
            for it in item:
                item_name = it.split(":")[0]
        x = i.split(" ")
        for z in x:
            if "x" in z:
                
                try:
                    nums = z.replace(",", "")
                    num = int(nums.replace("x", ""))
                    if item_name in Items:
                        i_num = Items[item_name] + num
                        Items[item_name] = i_num
                    else:
                        Items[item_name] = num
                except:
                    pass


    with open("Output.txt", "w+") as output:
        final = ""
        for i in Items:
            final += (str(Items[i])+ "x "+ i+"\n")
        output.write(final)
    for i in files:
        os.remove(i)


if __name__ == "__main__":
    Dropadd(["zz.txt"])
