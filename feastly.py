import openai, pathlib, re, os, heapq, codecs
from word2number import w2n

openai.api_key = "<Open AI API Key>"
data_dir = str(pathlib.Path(__file__).parent.resolve()) + "/archive/"

messages = [{"role": "system", "content": """"For each ingredient I don't list in my query, add a note at the end to tell me that I need to buy it also, don't put any
             text before or after the recipe (do not write "Title: ") and end it with the last step, make all recipes as detailed and verbose as possible, if the question is not cooking related, refuse to answer
             the first line of your response should be exclusively the title of the recipe"""},]

time_dict = {1 : "<30 minutes", 2 : "30 minutes to 1 hour", 3 : "<2 hours", 4 : "2+ hours"}

tag_dict = {1 :"Quick", 2 :"One-pot", 3 : "Fine-Dining", 4 :  "Molecular", 5 : "French-style", 6 : "Spanish", 7 : "Italian", 8 : "Mexican", 9 : "Chinese", 10 : "Spicy"}

additions_dict = {1 :"give an overview of the dish and ingredient choices", 2 :"give me some tips  about issues that might arise while cooking"}

def surveyor(keywords):
    res = []
    ref_table = []
    file_list = os.listdir(data_dir)
    hits = [0] * len(file_list)
    if len(file_list) == 1:
        return []
    for file in file_list:
        if file != ".DS_Store":
            ingredients = file.split(".")[0].split("_")
            ref_table.append(ingredients)
    for file in ref_table:
        if file != ".DS_Store":
            for word in keywords:
                if word in file:
                    hits[ref_table.index(file)] += 1
    selected = heapq.nlargest(2, range(len(hits)), key=hits.__getitem__)
    if hits[selected[1]] == 0:
        selected.pop(selected[1])
    for i in range(len(selected)):
        if (file_list[selected[i]] != ".DS_Store"):
            f = open(data_dir+file_list[selected[i]], "r")
            res.append(f.readline().strip('\n'))
    return res

def cooking_time():
    res = " which takes "
    print("What prep time are you looking for for this meal?")
    for time in time_dict:
        print("("+str(time)+") - " + time_dict[time])
    print(">", end =" ")
    response = input()
    res +=  time_dict[int(response)] + " to cook"
    return res

def tagger():
    res = " with tags like: "
    print("Are there any tags you would like to associate? (comma separated)")
    for tag in tag_dict:
        print("("+str(tag)+") - " + tag_dict[tag])
    print(">", end =" ")
    response = input().split(",")
    if response[0].strip() == "":
        return ""
    response = [r.strip() for r in response]
    for each in response:
        res +=  tag_dict[int(each)] + " "
    return res

def extras():
    res = " "
    print("Would you like to add any extra elements? (comma separated)")
    print("(1) - An overview of the dish and ingredient choices")
    print("(2) - Some tips about issues that might arise while cooking")
    print(">", end =" ")
    response = input().split(",")
    if response[0].strip() == "":
        return ""
    response = [r.strip() for r in response]
    for each in response:
        res +=  additions_dict[int(each)] + " "
    return res

def restrictions():
    negation = ["no", "nothing", "na", "n/a", "nada", "zilch", ""]
    res = ""
    print("Allergic to anything?")
    print(">", end =" ")
    allergens = input()
    if allergens.lower() not in negation:
        res += "I am allergic to:" + allergens
    print("Any other dietary restrictions?")
    print(">", end =" ")
    vs = input()
    if vs.lower() not in negation:
        res +=  " and I am " + vs
    return res

while(69):
    save = 0
    print(">", end =" ")
    prompt = input()
    if (prompt != ""):
        prompt = prompt.lower()
        msg = prompt
        if (msg == "!save"):
            save = 1
            output = codecs.open(data_dir+ "_".join(keywords) +".txt", "w", "utf-8")
            n = output.write(reply)
            output.close()
            pass
        if (msg != "!restart" and msg != "!save") :
            keywords = list(filter(None, re.split(",| ",msg)))
        if (len(messages) == 1) or (msg == "!restart"):
            if (msg == "!restart") :
                print(">", end =" ")
                prompt = input()
                prompt = prompt.lower()
                msg = prompt
                keywords = list(filter(None, re.split(",| ",msg)))
            time = cooking_time()
            restrict = restrictions()
            tags = tagger()
            adds = extras()
            msg = "Please give me a recipe with these ingredients: " + prompt + time + restrict + tags + adds
            if keywords != None:
                inspo = surveyor(keywords)
                if (inspo != []):
                    msg += " similar to these recipes: "
                    for i in range(len(inspo)):
                        msg += inspo[i]
                        if i < len(inspo)-1:
                            msg += " or "
        if save != 1 :
            messages.append({"role": "user", "content": msg})
            while(420):
                try:
                    chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
                    break
                except:
                    print("request failed, trying again")
                    pass
            reply = chat.choices[0].message.content
            messages.append({"role": "assistant", "content": reply})
            print("")
            print(reply)
            print("")