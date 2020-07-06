import discord
import random
from discord.ext import commands
from robiconf.bot_configuration import BotInstance

bot = BotInstance.bot #ngambil instance bot dari robiconf biar samaan sama robi.py
class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        await ctx.channel.send(f'{round(bot.latency*1000)}ms')

    @commands.command()
    @commands.cooldown(1, 5)
    async def code(self, ctx):
        i = 0
        kode = ""
        while i < 6:
            if i == 0: kode += str(random.randint(1,2))
            else: kode += str(random.randint(0,9))
            i += 1
        await ctx.channel.send(kode)

def setup(bot):
    bot.add_cog(Misc(bot))