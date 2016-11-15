import logging
import time
from discord.ext import commands

log = logging.getLogger(__name__)


class Mod:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def uptime(self):
        """Displays bot's total running time"""

        seconds = int(time.time() - self.bot.start_time)
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)

        def parse_time(time, time_type):
            if time > 1:
                return ' ' + str(time) + ' ' + time_type
            elif time == 1:
                return ' ' + str(time) + ' ' + time_type[:-1]
            else:
                return ''

        seconds = parse_time(seconds, 'seconds.')
        minutes = parse_time(minutes, 'minutes,')
        hours = parse_time(hours, 'hours,')
        days = parse_time(days, 'days,')

        output = "I have been up for{}{}{}{}".format(days, hours, minutes, seconds)
        await self.bot.say(output)

    @commands.command(pass_context=True)
    async def clear(self, ctx, number: int):

        channel = ctx.message.channel
        author = ctx.message.author
        server = author.server
        is_bot = self.bot.user.bot

        has_permissions = channel.permissions_for(server.me).manage_messages

        to_delete = []

        if not has_permissions:
            await self.bot.say('Not allowed to delete messages')
            return
        async for message in self.bot.logs_from(channel, limit=number + 1):
            to_delete.append(message)

        if is_bot:
            await mass_purge(self, to_delete)
        else:
            await slow_deletion(self, to_delete)

async def mass_purge(self, messages):
    while messages:
        if len(messages) > 1:
            await self.bot.delete_messages(messages[:100])
            messages = messages[100:]
        else:
            await self.bot.delete_message(messages[0])
            messages = []
        await self.asyncio.sleep(1.5)

async def slow_deletion(self, messages):
    for message in messages:
        try:
            await self.bot.delete_message(message)
        except:
            pass
        await self.asyncio.sleep(1.5)


def setup(bot):
    bot.add_cog(Mod(bot))
    log.info('Mod system set up complete.')
