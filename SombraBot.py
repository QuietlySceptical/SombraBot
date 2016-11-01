import asyncio
import random

import discord
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
    await bot.change_presence(game=discord.Game(name='Game Title'))


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
async def eightball(*message: str):
    lines = open("data/eightball.txt").read().splitlines()
    await bot.say('So you want to know: ' + ' ' .join(map(str, message)) + '\n ...Let me look into the future')
    await asyncio.sleep(3)
    await bot.say(random.choice(lines))


@bot.command(description='Response to porn')
async def porn():
    await bot.say('Look for it yourself!')


@bot.command(decription='A coin toss')
async def flip():
    outcome = random.randint(0, 1)
    if outcome == 0:
        outcome = "Heads"
    else:
        outcome = "Tails"
    await bot.say('Flipping the coin...')
    await asyncio.sleep(3)
    await bot.say('The coin shows, ' + outcome)


@bot.command()
async def hug(member: discord.Member):
    name = member.name
    hug = random.randrange(0, 3)
    if hug == 0:
        message = '(づ｡◕‿‿◕｡)づ ' + name
    elif hug == 1:
        message = '(っ˘̩╭╮˘̩)っ ' + name
    elif hug == 2:
        message = '(っಠ‿ಠ)っ ' + name
    elif hug == 3:
        message = '(づ￣ ³￣)づ ' + name
    await bot.say(message)

try:
    bot.run('token')
except KeyError:
    print("Environment variable not found.")