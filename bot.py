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

help_command = commands.DefaultHelpCommand(
    no_category = 'Commands'
)

intents = discord.Intents().all()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='r/',  help_command = help_command)
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

@bot.command(name="hello", brief="Say hello to the bot.", description="Make the bot say hello to you.")
async def ping(ctx):
    await ctx.send('Hello!')
@bot.command(name="inspire-me", brief="Make the bot inspire you.", description="Makes the bot send an inspireable quote using the zenquotes.io api.")
async def inspire_me(ctx):
    quote = get_quote()
    await ctx.send(quote)
@bot.command(name="meme", brief="Make the bot send a meme fresh from reddit.", description="Makes the bot send a meme from reddit using an API from http://meme-api.herokuapp.com/gimme")
async def send_meme(ctx):
    meme = gimme_meme()
    await ctx.send(meme)

@bot.command(name="ban", brief="Ban a member.", description="Ban a member. Can only be used by an adminstrator.")
@commands.has_permissions(administrator = True)
async def ban(ctx, member : discord.Member, *, reason = None):
    await member.ban(reason = reason)
    await ctx.send(f'Banned {member.mention}')

#The below code unbans player.
@bot.command(name="unban", brief="Unban a member.", description="Unban a member. Can only be used by an administrator.")
@commands.has_permissions(administrator = True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split("#")

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')
            return

@bot.command(name="kick", brief="Kicks a member.", description="Kicks a member. Can only be used by an administrator.")
@commands.has_permissions(administrator = True)
async def kick(ctx, member : discord.Member, *, reason = None):
    await member.kick(reason = reason)
    await ctx.send(f'Kicked {member.mention}')

bot.run(bot_token)
