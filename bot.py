import discord
from discord.ext import commands,tasks
import os
from dotenv import load_dotenv
import json
import requests
load_dotenv()

#print(os.getenv("DISCORD_TOKEN"))

bot_token = os.getenv("DISCORD_TOKEN")

size = len(bot_token)
bot_token = bot_token[:size - 2]

intents = discord.Intents().all()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='r/')
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


#@client.event
#async def on_message(message):
#    if message.content.startswith(sign + 'hello'):
#        await message.channel.send('Hello!')
#    if message.content.startswith(sign + 'inspire-me'):
#        quote = get_quote()
#        await message.channel.send(quote)
#    if message.content.startswith(sign + 'meme'):
#        meme = gimme_meme()
#        await message.channel.send(meme)
#    if message.content.startswith(sign + 'help'):
 #       embed=discord.Embed(title="REEEEEEEbot help", description="REEEEEEEbot is just an experiment made by REEEEEEEboi. Here are some commands: \n \n **r/hello** - Say hello to the bot \n \n **r/inspire-me** - make the bot send an inspirable quote \n \n **r/help** - You probably know what this one does :P \n \n **r/meme** - Give yourself a fresh meme from reddit. \n \n Well that's all for now, \n REEEEEEE", color=0xFF5733)

@commands.command()
async def hello(ctx):
    await ctx.send('Hello!')
@commands.command()
async def inspire_me(ctx):
    quote = get_quote()
    await ctx.send(quote)
@commands.command()
async def meme(ctx):
    meme = gimme_meme()
    await ctx.send(meme)

bot.add_command(hello)
bot.add_command(inspire_me)
bot.add_command(meme)

client.run(bot_token)
