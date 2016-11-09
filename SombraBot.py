import asyncio
import discord
import logging
import os
import random
import requests
import sys

from discord.ext import commands
from imgurpython import ImgurClient

try:
    import cogs.leveling
except ImportError as error:
    sys.exit("ERROR: Missing dependency: {0}".format(error))

log = logging.getLogger()
description = '''Sombra - A Simple Discord Bot'''
bot = commands.Bot(command_prefix='.', description=description, pm_help=True)
client = discord.Client()

try:
    imgurclient = ImgurClient(os.environ['IMGUR_CLIENT'], os.environ['IMGUR_SECRET'])
except KeyError:
    log.warn('Environment variable not found.')


initial_extensions = [
    'cogs.leveling'
]


@bot.event
async def on_ready():
    log.info("Logged in as {0} with ID {1}".format(bot.user.name, bot.user.id))


@bot.event
async def on_resumed():
    log.info('Sombra resumed...')


@bot.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('Hello Sombra'):
        msg = 'Hello {0.author.mention}'.format(message)
        await bot.send_message(message.channel, msg)

    elif message.content.startswith('Sombra'):
        msg = 'You called for me?'
        await bot.send_message(message.channel, msg)

    elif 'oberwath' in message.content.lower():
        msg = 'Darling, call it Overwatch'
        await bot.send_message(message.channel, msg)

    elif '@everyone' in message.content:
        msg = 'Hey kids, anyone want to buy some drugs?'
        await bot.send_message(message.channel, msg)

    elif '@241161319821082625' in message.content:  # Sombra
        with open('res/sombra.jpg', 'rb') as sombrapic:
            await bot.send_file(message.channel, sombrapic)

    elif '@146342721366392832' in message.content:  # Caffy
        msg = 'http://i.imgur.com/7JzpTQF.jpg'
        await bot.send_message(message.channel, msg)
    elif '@190912312427675649' in message.content:  # Thirith
        msg = 'I heard you like Guys & Dolls?'
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
    lines = open('data/compliment.txt').read().splitlines()
    await  bot.say(random.choice(lines))


@bot.command()
async def insult():
    """Gives a random insult"""
    lines = open('data/insult.txt').read().splitlines()
    await  bot.say(random.choice(lines))


@bot.command()
async def eightball(*message: str):
    """Ask a question and the EightBall will give an answer"""
    lines = open('data/eightball.txt').read().splitlines()
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
        outcome = 'Heads'
    else:
        outcome = 'Tails'
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
    else:
        message = "Oops, I can't pick a random number."
    await bot.say(message)


@bot.command()
async def owquick(username: str):
    """Overwatch Quick Play stats for a given player
    e.g. .owquick Hanzo#1234"""
    api_url = 'https://owapi.net/api/v3/u/{0}/stats'
    battlenet = username.replace('#', '-')
    headers = {'User-agent': 'SombraBot'}

    status = requests.get(api_url.format(battlenet), headers=headers)
    data = status.json()
    log.info("JSON status: %s" % status)

    prestige = data['eu']['stats']['quickplay']['overall_stats']['prestige']
    level = data['eu']['stats']['quickplay']['overall_stats']['level']
    time_played = data['eu']['stats']['quickplay']['game_stats']['time_played']
    wins = data['eu']['stats']['quickplay']['overall_stats']['wins']
    eliminations_avg = data['eu']['stats']['quickplay']['average_stats']['eliminations_avg']
    killsperdeath = data['eu']['stats']['quickplay']['game_stats']['kpd']
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
                          killsperdeath, healing_done_avg, offensive_assists_avg, defensive_assists_avg,
                          damage_done_avg, deaths_avg, time_spent_on_fire_avg))


@bot.command()
async def owcomp(username: str):
    """Overwatch Competitive stats for a given player
        e.g. .owcomp McCree#1234"""
    api_url = 'https://owapi.net/api/v3/u/{0}/stats'
    battlenet = username.replace('#', '-')
    headers = {'User-agent': 'SombraBot'}

    status = requests.get(api_url.format(battlenet), headers=headers)
    data = status.json()
    log.info("JSON status: %s" % status)

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


@bot.command()
async def cat():
    """Shows the user a random cat picture"""
    cat_url = requests.get('http://random.cat/meow')
    path = cat_url.json()

    picture = path['file']
    await bot.say(picture)


@bot.command()
async def penguin():
    """Shows the user a random penguin picture"""
    info = requests.get('http://penguin.wtf')
    await bot.say(info.content.decode('ascii'))


@bot.command()
async def imgrand():
    """Shows the user a random image from imgur"""
    rand = random.randint(0, 59)  # 60 results generated per page
    items = imgurclient.gallery_random(page=0)
    await bot.say(items[rand].link)


@bot.command()
async def imgsearch(*text: str):
    """Allows the user to search for an image from imgur"""
    rand = random.randint(0, 59)
    if text == ():
        await bot.say('Please enter a search term')
    elif text[0] != ():
        items = imgurclient.gallery_search(" ".join(text[0:len(text)]), advanced=None, sort='viral', window='all', page=0)
        if len(items) < 1:
            await bot.say('Your search gave no results')
        else:
            await bot.say(items[rand].link)


@bot.command()
async def imgtop(*text: str):
    """Shows the top image from a specified subrreddit"""
    if text == ():
        await bot.say('Please enter a subbreddit')
    elif text[0] != ():
        items = imgurclient.subreddit_gallery(" ".join(text[0:len(text)]), sort='top', window='day', page=0)
        if len(items) < 1:
            await bot.say('This subreddit section does not exist, try funny')
        else:
            await bot.say(items[0].link)


@bot.command()
async def imgnew(*text: str):
    """Shows the newest image from a specified subreddit"""
    if text == ():
        await bot.say('Please enter a subbreddit')
    elif text[0] != ():
        items = imgurclient.subreddit_gallery(" ".join(text[0:len(text)]), sort='time', window='day', page=0)
        if len(items) < 1:
            await bot.say('This subreddit section does not exist, try funny')
        else:
            await bot.say(items[0].link)


@bot.command(pass_context=True)
async def clear(ctx, number: int):

    channel = ctx.message.channel
    author = ctx.message.author
    server = author.server
    is_bot = bot.user.bot

    has_permissions = channel.permissions_for(server.me).manage_messages

    to_delete= []

    if not has_permissions:
        await bot.say('Not allowed to delete messages')
        return
    async for message in bot.logs_from(channel, limit=number + 1):
        to_delete.append(message)

    if is_bot:
        await mass_purge(to_delete)
    else:
        await slow_deletion(to_delete)


async def mass_purge(messages):
    while messages:
        if len(messages) > 1:
            await bot.delete_messages(messages[:100])
            messages = messages[100:]
        else:
            await bot.delete_message(messages[0])
            messages = []
        await asyncio.sleep(1.5)


async def slow_deletion(messages):
    for message in messages:
        try:
            await bot.delete_message(message)
        except:
            pass
        await asyncio.sleep(1.5)


async def change_presence_task():
    await bot.wait_until_ready()
    counter = 0
    while not client.is_closed:
        try:
            counter += 1
            lines = open('data/playing.txt').read().splitlines()
            playing = random.choice(lines)
            await bot.change_presence(game=discord.Game(name=playing))
            await asyncio.sleep(300)  # task runs every 120 seconds
        except FileNotFoundError:
            log.warn("File playing.txt was not found in the data directory.")


def load_modules():
    for extension in initial_extensions:
        try:
            log.info("Loading module: %s" % extension)
            bot.load_extension(extension)
        except Exception:
            log.warn("Failed to load module: %s" % extension)


if __name__ == '__main__':
    formatter = logging.Formatter("%(asctime)s [%(name)s] %(levelname)s: %(message)s")
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(formatter)
    log.addHandler(consoleHandler)

    logging.getLogger("discord").setLevel(logging.WARN)
    log.setLevel(logging.INFO)

    load_modules()
    bot.loop.create_task(change_presence_task())

    try:
        bot.run(os.environ['DISCORD_TOKEN'])
    except KeyError:
        log.warn('Environment variable not found.')
