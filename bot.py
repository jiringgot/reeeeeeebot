import discord
from discord.ext import commands,tasks
from discord.utils import get
import os
from dotenv import load_dotenv
import json
import requests
load_dotenv()

#print(os.getenv("DISCORD_TOKEN"))

bot_token = os.getenv("DISCORD_TOKEN")
count = os.getenv("count")
last_message = os.getenv('last_message')
og_statuses = os.environ.get("status")
statuses = og_statuses.split(" ")
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

ban_list = []
day_list = []
server_list = []

#This is a background process
async def countdown():
    await bot.wait_until_ready()
    while not bot.is_closed:
        await asyncio.sleep(1)
        day_list[:] = [x - 1 for x in day_list]
        for day in day_list:
            if day <= 0:
                try:
                    await bot.unban(server_list[day_list.index(day)], ban_list[day_list.index(day)])
                except:
                    print('Error! User already unbanned!')
                del ban_list[day_list.index(day)]
                del server_list[day_list.index(day)]
                del day_list[day_list.index(day)]

def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " - " + json_data[0]['a']
    return quote

def get_status():
    response = requests.get('http://reeeeeeebot.eu5.org/api.php')
    json_data = json.loads(response.text)
    return json_data

def gimme_meme():
    response = requests.get("http://meme-api.herokuapp.com/gimme")
    json_data = json.loads(response.text)
    quote = json_data
    return quote

def update_count():
    os.environ['count'] = str(count)
    print(str(count))

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
    reddit_arrows = bot.get_emoji(842372580920131614)
    embedVar = discord.Embed(title=meme['title'], description=" ", url=meme['postLink'], color=0x00ff00)
    embedVar.set_author(name=meme['author'])
    embedVar.set_image(url=meme['url'])
    embedVar.set_footer(text=str(meme['ups']))
    await ctx.send(embed=embedVar)

@bot.command(name="ban", brief="Ban a member.", description="Ban a member. Can only be used by an adminstrator.")
@commands.has_permissions(administrator = True)
@commands.has_role('staff')
async def ban(ctx, member : discord.Member, *, reason = None):
    await member.ban(reason = reason)
    

def check_status():
    global statuses, og_statuses
    returnList = []
    api_statuses = get_status()
    for i in range(len(api_statuses)):
        print(api_statuses[i]['status'])
        if statuses[i] != api_statuses[i]['status']:
            statuses[i] = api_statuses[i]['status']
            print(statuses[i])
            print(api_statuses[i])
            for i in range(len(statuses)):
                og_statuses += statuses[i]
            os.environ['status'] = og_statuses
            print(i)
            returnList.append(api_statuses[i])
    print(returnList)
    return returnList
    
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
@commands.has_role("staff")
async def kick(ctx, member : discord.Member, *, reason = None):
    await member.kick(reason = reason)
    await ctx.send(f'Kicked {member.mention}')


@bot.command(name="status")
async def status(ctx):
    temp_statuses = check_status()
    for i in range(len(temp_statuses)):
        print(temp_statuses)
        await ctx.send(temp_statuses[i]['name'] + ' is now ' + temp_statuses[i]['status'])
    
@bot.event
async def on_message(message):
    global count, last_message
    if(message.author == bot.user):
        return
    if message.channel == bot.get_channel(843246928161669141):
        print(last_message)
        if message.author == last_message:
            count = 0
            print('Same author, starting over')
            await message.channel.send('Same author, starting over')
            update_count()
        if message.content == str(count):
            count = int(count) + 1
            print('Counted')
            update_count()
            last_message = message.author
            return
        else:
            count = 0
            print('Wrong number, starting over')
            await message.channel.send('Wrong number, starting over')
            update_count()
            return
    await bot.process_commands(message)
bot.run(bot_token)
