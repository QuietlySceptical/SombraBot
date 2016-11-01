import asyncio
import random

import requests
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


@bot.command(description='Average player stats for Overwatch user')
async def owquickplay(username: str):
    api_url = 'https://owapi.net/api/v3/u/{0}/stats'
    battlenet = username.replace('#', '-')
    headers = {'User-agent': 'SombraBot'}

    status = requests.get(api_url.format(battlenet), headers=headers)
    data = status.json()
    print(status)

    prestige = data['eu']['stats']['quickplay']['overall_stats']['prestige']
    level = data['eu']['stats']['quickplay']['overall_stats']['level']
    time_played = data['eu']['stats']['quickplay']['game_stats']['time_played']
    wins = data['eu']['stats']['quickplay']['overall_stats']['wins']
    eliminations_avg = data['eu']['stats']['quickplay']['average_stats']['eliminations_avg']
    killperdeath = data['eu']['stats']['quickplay']['game_stats']['kpd']
    healing_done_avg = data['eu']['stats']['quickplay']['average_stats']['healing_done_avg']
    offensive_assists_avg = data['eu']['stats']['quickplay']['average_stats']['offensive_assists_avg']
    defensive_assists_avg = data['eu']['stats']['quickplay']['average_stats']['defensive_assists_avg']
    damage_done_avg = data['eu']['stats']['quickplay']['average_stats']['damage_done_avg']
    deaths_avg = data['eu']['stats']['quickplay']['average_stats']['deaths_avg']
    time_spent_on_fire_avg = data['eu']['stats']['quickplay']['average_stats']['time_spent_on_fire_avg']

    await bot.say('```Quick Play stats for {0}\n'
                  'Presitige: {1}\n'
                  'Level: {2}\n'
                  'Time Played: {3}\n'
                  'Wins: {4}\n\n'
                  'Avg Eliminations: {5}\n'
                  'KPD: {6}\n'
                  'Avg Healing Done: {7}\n'
                  'Avg Offensive Assists: {8}\n'
                  'Avg Defensive Assists: {9}\n'
                  'Avg Damage Done: {10}\n'
                  'Avg Deaths: {11}\n'
                  'Avg Time on Fire: {12}\n'
                  '```'
                  .format(username, prestige, level, time_played, wins, eliminations_avg,
                          killperdeath, healing_done_avg, offensive_assists_avg, defensive_assists_avg,
                          damage_done_avg, deaths_avg, time_spent_on_fire_avg))


try:
    bot.run('token')
except KeyError:
    print("Environment variable not found.")