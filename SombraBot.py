import asyncio
import discord
import logging
import random
import sys
import time

from discord.ext import commands

try:
    import cogs.overwatch
    import cogs.image
    import cogs.mod
    import cogs.chance
    import cogs.social
    import cogs.music

except ImportError as error:
    sys.exit("ERROR: Missing dependency: {0}".format(error))

log = logging.getLogger()
description = '''Sombra - A Simple Discord Bot'''
bot = commands.Bot(command_prefix='.', description=description, pm_help=True)
client = discord.Client()

initial_extensions = [
    'cogs.overwatch',
    'cogs.image',
    'cogs.mod',
    'cogs.chance',
    'cogs.social',
    'cogs.music'
]


@bot.event
async def on_ready():
    log.info("Logged in as {0} with ID {1}".format(bot.user.name, bot.user.id))
    bot.start_time = time.time()


@bot.event
async def on_resumed():
    log.info('Sombra resumed...')


@bot.event
async def on_command_error(error, ctx):
    if isinstance(error, commands.NoPrivateMessage):
        await bot.send_message(ctx.message.author,
                               '[ERROR: NoPrivateMessage] Sorry. This command cannot be used in private messages.')
    elif isinstance(error, commands.DisabledCommand):
        await bot.send_message(ctx.message.channel,
                               '[ERROR: DisabledCommand] Sorry. This command is disabled and can\'t be used.')
    elif isinstance(error, commands.CheckFailure):
        await bot.send_message(ctx.message.channel,
                               '[ERROR: CheckFailure] Sorry. You don\'t have permission to run this command.')
    elif isinstance(error, commands.CommandNotFound):
        await bot.send_message(ctx.message.channel,
                               '[ERROR: CmdNotFound] Sorry. The comand your requested doesn\'t exist.')


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
        try:
            with open('res/sombra.jpg', 'rb') as sombrapic:
                await bot.send_file(message.channel, sombrapic)
        except FileNotFoundError:
            log.warn("Sombra.jpg was not found in the resources folder.")

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


@bot.command(description='Response to porn')
async def porn():
    await bot.say('Look for it yourself!')


@bot.command()
async def reverse(*, text: str):
    to_reverse = text
    await bot.say(str(to_reverse)[::-1])


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
        bot.run('Discord Token')
    except KeyError:
        log.warn('Environment variable not found.')
