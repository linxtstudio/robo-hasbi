from discord.ext import commands
from discord import Embed
from helpers import get_anonymous_channel
from helpers.ui import UI
from random import randint

class PrivateCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.dm_only()
    @commands.command(aliases=['k'])
    async def kokuhaku(self, ctx, *, kokuhaku: str):
        channel = get_anonymous_channel(self.bot)
        
        async with ctx.typing():
            koku_embed = Embed(color=randint(0, 0xffffff))
            koku_embed.add_field(name='Kokuhaku', value=kokuhaku)
            await channel.send(embed=koku_embed)
            await ctx.send(embed=UI.success_embed("Kokuhaku kamu sudah dikirim secara anonymous"))


def setup(bot):
    bot.add_cog(PrivateCommands(bot))