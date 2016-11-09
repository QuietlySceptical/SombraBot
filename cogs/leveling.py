from discord.ext import commands


class Level:
    def __init__(self, bot):
        self.bot = bot


@commands.group(pass_context=True)
async def rank(self, ctx):
    if ctx.invoked_subcommand is None:
        await self.bot.say('Incorrect subcommand passed.')


@rank.command()
async def join(bot):
    """Join the ranking system"""
    await bot.send_message('join')


def setup(self):
    self.add_cog(Level(self))
    print('level setup')
