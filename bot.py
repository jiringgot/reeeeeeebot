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


@bot.event
async def on_ready():
    print('Bot is ready.')
    await bot.change_presence(activity=discord.Streaming(name="Tiredcheeseboi | r/help", url='https://twitch.tv/tiredcheeseboi'))

@bot.command(name="hello", help_description="Say hello")
async def ping(ctx):
    await ctx.send('Hello!')
@bot.command(name="inspire-me")
async def inspire_me(ctx):
    quote = get_quote()
    await ctx.send(quote)
@bot.command(name="meme")
async def send_meme(ctx):
    meme = gimme_meme()
    await ctx.send(meme)

bot.run(bot_token)
