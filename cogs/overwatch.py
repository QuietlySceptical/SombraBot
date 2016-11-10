import logging

from urllib.request import Request, urlopen

import requests
from discord.ext import commands

log = logging.getLogger(__name__)


class Overwatch:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def owquick(self, ctx, battlenet):
        """Overwatch Quick Play stats for a given player
        e.g. .owquick Hanzo#1234"""
        api_url = 'https://owapi.net/api/v3/u/{0}/stats'
        battlenet_for_api = battlenet.replace('#', '-')
        headers = {'User-agent': 'SombraBot'}

        status = requests.get(api_url.format(battlenet_for_api), headers=headers)
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

        await self.bot.say('```Quick Play stats for {0}\n'
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
                           .format(battlenet, prestige, level, time_played, wins, eliminations_avg,
                                   killsperdeath, healing_done_avg, offensive_assists_avg, defensive_assists_avg,
                                   damage_done_avg, deaths_avg, time_spent_on_fire_avg))

    @commands.command(pass_context=True)
    async def owcomp(self, ctx, battlenet):
        """Overwatch Competitive stats for a given player
            e.g. .owcomp McCree#1234"""
        api_url = 'https://owapi.net/api/v3/u/{0}/stats'
        battlenet_for_api = battlenet.replace("#", "-")

        print(battlenet_for_api)

        req = Request(api_url.format(battlenet_for_api))
        req.add_header('User-agent', 'SombraBot')
        status = urlopen(req).read()
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

        await self.bot.say('```Competitive stats for {0}\n'
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
                           .format(battlenet, comprank, games_played, win_rate, wins, losses, eliminations_avg,
                                   killperdeath, healing_done_avg, offensive_assists_avg, defensive_assists_avg,
                                   damage_done_avg, deaths_avg, time_spent_on_fire_avg))


def setup(bot):
    bot.add_cog(Overwatch(bot))
    log.info('Overwatch system set up complete.')
