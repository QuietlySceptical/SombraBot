import logging
import random

import discord
from discord.ext import commands

log = logging.getLogger(__name__)


class Social:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def compliment(self):
        """Gives a random compliment"""
        lines = open('data/compliment.txt').read().splitlines()
        await  self.bot.say(random.choice(lines))

    @commands.command(pass_context=True)
    async def insult(self):
        """Gives a random insult"""
        lines = open('data/insult.txt').read().splitlines()
        await  self.bot.say(random.choice(lines))

    @commands.command(pass_context=True)
    async def hug(self, ctx, member: discord.Member):
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
        await self.bot.say(message)


def setup(bot):
    bot.add_cog(Social(bot))
    log.info('Social system set up complete.')
