from discord.ext import commands
import discord
import logging

if discord.opus.is_loaded() is False:
    discord.opus.load_opus('opus')

log = logging.getLogger(__name__)


class Voice:

    def __init__(self, bot):
        self.bot = bot
        self.player = None
        self.voice = None

    @commands.command(pass_context=True, no_pm=True)
    async def summon(self, ctx):

        channel = ctx.message.author.voice_channel

        if channel is None:
            await self.bot.say("Don't be antisocial, join a voice channel!")
            return False
        else:

            if self.voice is None:
                await self.bot.say('Joining {}'.format(channel))
                self.voice = voice = await self.bot.join_voice_channel(channel)
            else:
                await self.bot.say('Moving to {}'.format(channel))
                await self.voice.move_to(channel)
            return True

    @commands.command(pass_context=True, no_pm=True)
    async def play(self, ctx, *, song: str):

        voice = self.voice

        opts = {
            'default_search': 'auto',
            'quiet': True,
        }

        if voice is None:
            await ctx.invoke(self.summon)
        try:
           self.player = player = await voice.create_ytdl_player(song, ytdl_options=opts)
        except Exception as e:
            fmt = 'An error occurred while processing this request: ```py\n{}: {}\n```'
            await self.bot.send_message(ctx.message.channel, fmt.format(type(e).__name__, e))
        else:
            player.volume = 0.6
            message = 'Playing {0}'.format((player.title))
            await self.bot.say(message)
            player.start()

    @commands.command(pass_context=True, no_pm=True)
    async def volume(self, ctx, value: int):
        player = self.player
        if player.is_playing():
            player.volume = value / 100
            await self.bot.say('Set the volume to {:.0%}'.format(player.volume))
        else:
            await self.bot.say('There is nothing playing')

    @commands.command(pass_context=True, no_pm=True)
    async def pause(self, ctx):
        player = self.player
        if player.is_playing():
            player.pause()
            log.info("Paused")

    @commands.command(pass_context=True, no_pm=True)
    async def resume(self, ctx):
        player = self.player
        if not player.is_playing():
            player.resume()

    @commands.command(pass_context=True, no_pm=True)
    async def stop(self, ctx):
        server = ctx.message.server
        player = self.player
        voice = self.voice

        if player.is_playing():
            player.stop()

        try:
            await self.voice.disconnect()
            self.voice = None
        except Exception as e:
            fmt = 'An error occurred while processing this request: ```py\n{}: {}\n```'
            await self.bot.send_message(ctx.message.channel, fmt.format(type(e).__name__, e))

    # TODO add a current song
    @commands.command(pass_context=True)
    async def playing(self, ctx):
        """Shows info about the currently played song."""

        player = self.player

        if player.current is None:
            await self.bot.say('Not playing anything.')
        else:
            await self.bot.say('Now playing {} :'.format(player.current))


def setup(bot):
    bot.add_cog(Voice(bot))
    log.info('Music system set up complete')
