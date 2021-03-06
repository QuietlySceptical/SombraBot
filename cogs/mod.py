import logging
import time
import discord
from discord.ext import commands
from utils import checks

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
    async def info(self, ctx, member : discord.Member = None):
        if member == None:
            member = ctx.message.author
        await self.bot.say('```xl\n' +
                           'Name: {0.name}\n'.format(member) +
                           'Joined Server: {0.joined_at}\n'.format(member) +
                           'ID: {0.id}\n'.format(member) +
                           'Has existed since: {0.created_at}\n'.format(member) +
                           'Bot?: {0.bot}\n'.format(member) +
                           '```' +
                           '\n{0.avatar_url}'.format(member))

    @commands.command(pass_context=True)
    @checks.mod_or_permissions(administrator=True)
    async def avatar(self):
        with open('res/skull.png', 'rb') as image:
            image = image.read()
            await self.bot.edit_profile(avatar=image)
            await self.bot.say('My avatar had been changed')

    @commands.command(pass_context=True)
    @checks.mod_or_permissions(administrator=True)
    async def username(self):
        name = "Sombra"
        await self.bot.edit_profile(username=name)
        await self.bot.say("My name has been changed!")

    @commands.command(pass_context=True)
    @checks.mod_or_permissions(administrator=True)
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
