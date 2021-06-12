from discord.ext import commands
from discord import Embed

class PrivateCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.dm_only()
    @commands.command(aliases=['k'])
    async def kokuhaku(self, ctx, *, kokuhaku: str):
        channel = self.bot.get_channel(853144744678916136)
        
        async with ctx.typing():
            koku_embed = Embed(color=0xffffff)
            koku_embed.add_field(name='Kokuhaku', value=kokuhaku)
            await channel.send(embed=koku_embed)

            await ctx.send('Kokuhaku kamu sudah dikirim secara anonymous')


def setup(bot):
    bot.add_cog(PrivateCommands(bot))