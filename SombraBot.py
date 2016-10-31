import random

from discord.ext import commands

description = '''Sombra - A Simple Discord Bot'''

bot = commands.Bot(command_prefix='.',
                   description=description)


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.command()
async def add(left: int, right: int):
    """Adds two numbers together"""
    await bot.say(left + right)


@bot.command(description='makes a choice')
async def choose(*choices: str):
    """Chooses between multiple choices"""
    await bot.say(random.choice(choices))


try:
    bot.run('token')
except KeyError:
    print("Environment variable not found.")