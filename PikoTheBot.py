import os
import discord
import random
import json
from pip._vendor import requests

client = discord.Client()
# client is the connection to Discord

def getInspireFromAPI():
    response = requests.get('https://zenquotes.io/api/random')
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return quote


def getTriviaFromAPI():
    response = requests.get('https://opentdb.com/api.php?amount=1')
    json_data = json.loads(response.text)
    return json_data


# we use Client.event() decorator to register an event
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
# on_ready() event is called when the bot has finished logging in and setting things up - runs always

@client.event
async def on_message(message):
    lower = message.content.lower()

    # for greetings
    if message.author == client.user:  # ignore message by ourselves
        return
    if lower.startswith('~hello'):
        await message.channel.send('Hello, this yo boi Piko')

    # for help guide
    if lower.startswith('~help'):
        embedVar = discord.Embed(title="Piko Help Section", description="Here are some commands you can use on me!",
                                 color=0x546e7a)
        embedVar.add_field(name="~cal", value="To perform calculations. Ex - ~cal 6*234", inline=False)
        embedVar.add_field(name="~roll", value="To roll a dice.", inline=False)
        embedVar.add_field(name="~valid <Name>", value="To see how valid <Name> is.", inline=False)
        embedVar.add_field(name="~inspire", value="For me to inspire you.", inline=False)
        await message.channel.send(embed=embedVar)

    # for calculations
    if message.content.startswith('~cal'):
        content = message.content.strip().replace("~cal", "")
        if "**" in content:
            await message.channel.send('Currently fixing issues with the power operator!')
        elif "/0" in content:
            await message.channel.send("That's a math error.")
        else:
            answer = eval(content)
            embedVar = discord.Embed(title="Answer", description=str(answer), color=0x546e7a)
            await message.channel.send(embed=embedVar)

    # for rolling dice
    if message.content.startswith('~roll'):
        await message.channel.send('Rolling Dice...')
        embedVar = discord.Embed(title="Dice Rolled!", description=random.randint(1, 7), color=0x546e7a)
        await message.channel.send(embed=embedVar)

    # for checking how valid you are
    if lower.startswith('~valid'):
        content = (lower.split(" "))[-1]
        await message.channel.send('Talking to the valid gods...')

        if content == 'yasinda':
            embedVar = discord.Embed(title="The gods have spoken!", description=content + " is 100% valid",
                                     color=0x546e7a)
            await message.channel.send(embed=embedVar)
        elif content == 'piko':
            embedVar = discord.Embed(title="The gods have spoken!", description="I'm the most valid", color=0x546e7a)
            msg = await message.channel.send(embed=embedVar)
            await msg.add_reaction('🥵')
            await msg.add_reaction('🥺')
        else:
            embedVar = discord.Embed(title="The gods have spoken!",
                                     description=content + " is " + str(random.randint(1, 101)) + "% valid",
                                     color=0x546e7a)
            await message.channel.send(embed=embedVar)

    # for returning random inspo quote
    if lower.startswith('~inspire'):
        quote = getInspireFromAPI()
        await message.channel.send("Googling inspiring quotes...")
        embedVar = discord.Embed(description=quote, color=0x546e7a)
        await message.channel.send(embed=embedVar)

    # trivia from API
    if lower.startswith('~trivia'):
        trivia_body = getTriviaFromAPI()
        answer = str(trivia_body['results'][0]['correct_answer'])
        set_of_answers = trivia_body['results'][0]['incorrect_answers']
        set_of_answers.append(trivia_body['results'][0]['correct_answer'])
        random.shuffle(set_of_answers)

        embedVar = discord.Embed(title="Trivia Challenge!", description=str(trivia_body['results'][0]['question']),
                                 color=0x546e7a)
        count = 1

        for ans in set_of_answers:
            embedVar.add_field(name="Option " + str(count), value=ans, inline=False)
            count += 1

        await message.channel.send(embed=embedVar) #only needs var if you want to do something with the output of piko's embedded message

        @client.event #find a way to respond to users answer
        async def on_message(user_answer):
            if user_answer.lower == answer.lower():
                embedVar1 = discord.Embed(description="You got it right!", color=0x546e7a)
                await message.channel.send(embed=embedVar1)

            else:
                embedVar1 = discord.Embed(description="You got it wrong :(", color=0x546e7a)
                await message.channel.send(embed=embedVar1)


#Token for chatbot
# client.run(os.environ['TOKEN'])
#OR
#client.run('ADD YOUR TOKEN HERE')

# NOTES:
# message.content is just a string in python
