import discord
from discord.ext import commands,tasks
import os
from dotenv import load_dotenv
import json
load_dotenv()

#print(os.getenv("DISCORD_TOKEN"))

bot_token = os.getenv("DISCORD_TOKEN")

size = len(bot_token)
bot_token = bot_token[:size - 2]

intents = discord.Intents().all()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='r/',intents=intents)
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


@vot.event
async def on_ready():
    await client.change_presence(
        activity=discord.Activity(type=discord.ActivityType.watching, name="TiredCheeseBoi on Twitch | r/help"))
    print('We have logged in as {0.user}'.format(client))


@bot.command(name='hello', help='Say hello to the bot')
async def hello(ctx):
    await ctx.send('Hello!')
    return
@bot.command(name='inspire-me', help='Send an inspirable quote')
async def inspire_me(ctx):
    quote = get_quote()
    await ctx.send(quote)
    return
@bot.command(name='meme', help='Make the bot send a meme')
async def meme(ctx):
    quote = gimme_meme()
    await ctx.send(quote)


client.run(bot_token)
