import logging
import random

import time
from discord.ext import commands

log = logging.getLogger(__name__)


class Chance:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def choose(self, ctx,  *choices: str):
        """Chooses between items in a list"""
        await self.bot.say(random.choice(choices))

    @commands.command(pass_context=True)
    async def eightball(self, ctx, *message: str):
        """Ask a question and the EightBall will give an answer"""
        lines = open('data/eightball.txt').read().splitlines()
        await self.bot.say('So you want to know: ' + ' '.join(map(str, message)) + '\n ...Let me look into the future')
        await self.bot.send_typing(ctx.message.channel)
        time.sleep(1)
        await self.bot.say(random.choice(lines))

    @commands.command(pass_context=True)
    async def flip(self, ctx):
        """Flips a coin, resulting in Heads or Tails"""
        outcome = random.randint(0, 1)
        if outcome == 0:
            outcome = 'Heads'
        else:
            outcome = 'Tails'
        await self.bot.say('Flipping the coin...')
        await self.bot.send_typing(ctx.message.channel)
        time.sleep(1)
        await self.bot.say('The coin shows, ' + outcome)


def setup(bot):
    bot.add_cog(Chance(bot))
    log.info('Chance system set up complete.')
