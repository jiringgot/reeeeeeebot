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


class Bot(commands.AutoShardedBot):

    def __init__(self):
        super().__init__(command_prefix="r/")
        self.add_command(commands.Command(self.hello, name="hello"))
        self.add_command(commands.Command(self.inspire_me, name="inspire-me"))

    async def hello(self, ctx):
        await ctx.send('Hello!')
    async def inspire_me(self, ctx):
        quote = get_quote()
        await ctx.send(quote)
    
    def run(self):
        super().run(bot_token)


if __name__ == "__main__":
    bot = Bot()
    bot.run()
