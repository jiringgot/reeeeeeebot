import discord
import os

try:
    os.system('pip install requests')
    import requests
except error as e:
    print(e)
import json

print(os.getenv("DISCORD_TOKEN"))

bot_token = os.getenv("DISCORD_TOKEN")

client = discord.Client()
sign = 'r/'

changelog_message = False



def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " - " + json_data[0]['a']
    return quote


def gimme_meme():
    response = requests.get("http://meme-api.herokuapp.com/gimme")
    json_data = json.loads(response.text)
    quote = json_data['url']
    return quote


@client.event
async def on_ready():
    await client.change_presence(
        activity=discord.Activity(type=discord.ActivityType.watching, name="TiredCheeseBoi on Twitch | r/help"))
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    global changelog_message
    if message.author == client.user:
        return
    if message.content.startswith(sign + 'hello'):
        print('Sent Message: Hello!')
        await message.channel.send('Hello!')

    if message.content.startswith(sign + 'inspire-me'):
        quote = get_quote()
        print('Sent message: ' + quote)
        await message.channel.send(quote)

    if message.content.startswith(sign + 'help'):
        embed = discord.Embed(title="REEEEEEEbot Help",
                              description="REEEEEEEbot is just an experiment made by REEEEEEEboi. Here are some commands: \n \n **r/hello** - Say hello to the bot \n \n **r/inspire-me** - make the bot send an inspirable quote \n \n **r/help** - You probably know what this one does :P \n \n **r/meme** - Give yourself a fresh meme from reddit. \n \n Well that's all for now, \n REEEEEEE",
                              color=discord.Colour.blue())
        await message.channel.send(embed=embed)

    if message.content.startswith(sign + 'changelog'):
        await message.channel.send('Send message below')
        changelog_message = True
        return

    if message.content.startswith(sign + 'stop') and changelog_message:
        await message.channel.send('Stopped')
        changelog_message = False
        return

    if changelog_message == True:
        embed = discord.Embed(title="Changelog", description=message.content, color=discord.Colour.red())
        channel = client.get_channel(794289983186927626)
        await channel.send(embed=embed)

    if message.content.startswith(sign + 'meme'):
        image = gimme_meme()
        await message.channel.send(image)

    if message.content.startswith(sign + 'kick'):
        message.author.kick(reason=None)


client.run(bot_token)
