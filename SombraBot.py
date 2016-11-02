import asyncio
import random

import requests
import discord
from discord.ext import commands

description = '''Sombra - A Simple Discord Bot'''

bot = commands.Bot(command_prefix='.',
                   description=description, pm_help=True)

client = discord.Client()


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(game=discord.Game(name='Game Title'))


@bot.event
async def on_message(message):
    print('test')
    if message.author == client.user:
        return

    if message.content.startswith('Hello Sombra'):
        msg = 'Hello {0.author.mention}'.format(message)
        await bot.send_message(message.channel, msg)
    elif message.content.startswith('Sombra'):
        msg = 'You called for me?'.format(message)
        await bot.send_message(message.channel, msg)
    elif 'Oberwath' or 'oberwath' in message.content:
        msg = 'Darling, call it Overwatch'
        await bot.send_message(message.channel, msg)
    elif '@everyone' in message.content:
        msg = 'Hey kids, anyone want to buy some drugs?'
        await bot.send_message(message.channel, msg)

    await bot.process_commands(message)


@bot.command()
async def add(left: int, right: int):
    """Adds two number together"""
    await bot.say(left + right)


@bot.command()
async def choose(*choices: str):
    """Chooses between items in a list"""
    await bot.say(random.choice(choices))


@bot.command()
async def compliment():
    """Gives a random compliment"""
    lines = open("data/compliment.txt").read().splitlines()
    await  bot.say(random.choice(lines))


@bot.command()
async def insult():
    """Gives a random insult"""
    lines = open("data/insult.txt").read().splitlines()
    await  bot.say(random.choice(lines))


@bot.command()
async def eightball(*message: str):
    """Ask a question and the EightBall will give an answer"""
    lines = open("data/eightball.txt").read().splitlines()
    await bot.say('So you want to know: ' + ' ' .join(map(str, message)) + '\n ...Let me look into the future')
    await asyncio.sleep(3)
    await bot.say(random.choice(lines))


@bot.command(description='Response to porn')
async def porn():
    await bot.say('Look for it yourself!')


@bot.command()
async def flip():
    """Flips a coin, resulting in Heads or Tails"""
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
    """Have a hug"""
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


@bot.command()
async def owquick(username: str):
    """Overwatch Quick Play stats for a given player
    e.g. -owquick Hanzo#1234"""
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
                  'Prestige: {1}\n'
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


@bot.command(description='Average player stats for Overwatch user')
async def owcomp(username: str):
    """Overwatch Competitive stats for a given player
        e.g. -owcomp McCree#1234"""
    api_url = 'https://owapi.net/api/v3/u/{0}/stats'
    battlenet = username.replace('#', '-')
    headers = {'User-agent': 'SombraBot'}

    status = requests.get(api_url.format(battlenet), headers=headers)
    data = status.json()
    print(status)

    comprank = data['eu']['stats']['competitive']['overall_stats']['comprank']
    games_played = data['eu']['stats']['competitive']['game_stats']['games_played']
    win_rate = data['eu']['stats']['competitive']['overall_stats']['win_rate']
    wins = data['eu']['stats']['competitive']['overall_stats']['wins']
    losses = data['eu']['stats']['competitive']['overall_stats']['losses']
    eliminations_avg = data['eu']['stats']['competitive']['average_stats']['eliminations_avg']
    killperdeath = data['eu']['stats']['competitive']['game_stats']['kpd']
    healing_done_avg = data['eu']['stats']['competitive']['average_stats']['healing_done_avg']
    offensive_assists_avg = data['eu']['stats']['competitive']['average_stats']['offensive_assists_avg']
    defensive_assists_avg = data['eu']['stats']['competitive']['average_stats']['defensive_assists_avg']
    damage_done_avg = data['eu']['stats']['competitive']['average_stats']['damage_done_avg']
    deaths_avg = data['eu']['stats']['competitive']['average_stats']['deaths_avg']
    time_spent_on_fire_avg = data['eu']['stats']['competitive']['average_stats']['time_spent_on_fire_avg']

    await bot.say('```Competitive stats for {0}\n'
                  'Rank: {1}\n'
                  'Games Played: {2}\n'
                  'Win Rate: {3}\n'
                  'Wins: {4}\n'
                  'Losses: {5}\n\n'
                  'Avg Eliminations: {6}\n'
                  'KPD: {7}\n'
                  'Avg Healing Done: {8}\n'
                  'Avg Offensive Assists: {9}\n'
                  'Avg Defensive Assists: {10}\n'
                  'Avg Damage Done: {11}\n'
                  'Avg Deaths: {12}\n'
                  'Avg Time on Fire: {13}\n'
                  '```'
                  .format(username, comprank, games_played, win_rate, wins, losses, eliminations_avg,
                          killperdeath, healing_done_avg, offensive_assists_avg, defensive_assists_avg,
                          damage_done_avg, deaths_avg, time_spent_on_fire_avg))


try:
    bot.run('token')
except KeyError:
    print("Environment variable not found.")