import logging
from discord.ext import commands

log = logging.getLogger(__name__)


class Level:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def rank(self, ctx):
        if ctx.invoked_subcommand is None:
            await self.bot.say('Incorrect subcommand passed.')

    @commands.command(pass_context=True)
    async def join(self, bot):
        """Join the ranking system"""
        await self.bot.say('join')


def setup(bot):
    bot.add_cog(Level(bot))
    log.info('Levelling system set up complete.')
