import random

from discord.ext import commands

description = '''Sombra - A Simple Discord Bot'''

bot = commands.Bot(command_prefix='-',
                   description=description)


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.command(description='adds two numbers')
async def add(left: int, right: int):
    await bot.say(left + right)


@bot.command(description='makes a choice')
async def choose(*choices: str):
    await bot.say(random.choice(choices))


@bot.command(description='have a compliment')
async def compliment():
    lines = open("data/compliment.txt").read().splitlines()
    await  bot.say(random.choice(lines))


@bot.command(description='have an insult')
async def insult():
    lines = open("data/insult.txt").read().splitlines()
    await  bot.say(random.choice(lines))


@bot.command(description='8 ball')
async def eightball():
    lines = open("data/eightball.txt").read().splitlines()
    await bot.say(random.choice(lines))


try:
    bot.run('token')
except KeyError:
    print("Environment variable not found.")