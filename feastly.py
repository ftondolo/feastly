import openai
from word2number import w2n

openai.api_key = "<Open AI API Key>"

messages = [{"role": "system", "content": """"For each ingredient I don't list in my query, add a note at the end to tell me that I need to buy it also, don't put any
             text before or after the recipe (do not write "Title: ") and end it with the last step, make all recipes detailed, if the question is not cooking related, refuse to answer"""},]

time_dict = {1 : "<30 minutes", 2 : "30 minutes to 1 hour", 3 : "<2 hours", 4 : "2+ hours"}

tags = {1 :"Quick", 2 :"One-pot", 3 : "Fine-Dining", 4 :  "Molecular", 5 : "French-style", 6 : "Spanish", 7 : "Italian", 8 : "Mexican", 9 : "Chinese", 10 : "Spicy"}

additions = {1 :"give an overview of the dish and ingredient choices", 2 :"give me some tips  about issues that might arise while cooking"}

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
    for tag in tags:
        print("("+str(tag)+") - " + tags[tag])
    print(">", end =" ")
    response = input().split(",")
    if response[0].strip() == "":
        return ""
    response = [r.strip() for r in response]
    for each in response:
        res +=  tags[int(each)] + " "
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
        res +=  additions[int(each)] + " "
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
    print(">", end =" ")
    prompt = input()
    if (prompt != ""):
        prompt = prompt.lower()
        msg = prompt
        if (len(messages) == 1):
            time = cooking_time()
            restrict = restrictions()
            tags = tagger()
            adds = extras()
            msg = "Please give me a recipe with these ingredients: " + prompt + time + restrict + tags + adds
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

