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

bot.remove_command('help')

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

@bot.command(name="hello")
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

@bot.command(name='help')
async def help(ctx):
    embed=discord.Embed(title="Help", description="Here is help:", color=0x00ff00)
    embed.add_field(name="r/hello", value="Say hello to the bot", inline=False)
    embed.add_field(name="r/inspire-me", value="Make the bot say an inspirable quote", inline=False)
    embed.add_field(name="r/meme", value="Make the bot send a meme fresh from reddit", inline=False)
    author = ctx.message.author
    msg = await bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
    author = msg.author
    await bot.send_message(author, embed=embed)
    
async def on_message(message):
    if message.startswith(sign + 'help'):
        embed=discord.Embed(title="Help", description="Here is help:", color=0x00ff00)
        embed.add_field(name="r/hello", value="Say hello to the bot", inline=False)
        embed.add_field(name="r/inspire-me", value="Make the bot say an inspirable quote", inline=False)
        embed.add_field(name="r/meme", value="Make the bot send a meme fresh from reddit", inline=False)
        await message.author.send(embed)

bot.run(bot_token)
