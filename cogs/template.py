# pastikan ekstensi cogs kalian .py ya :)

import discord
from discord.ext import commands

class Template(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['temp']) #nama lain dari command
    async def template(self, ctx): #karena ini didalam kelas, semua fungsi harus punya argumen 'self'
        await ctx.channel.send('Ini Command Template')


def setup(bot): #mendaftarkan cogs
    bot.add_cog(Template(bot)) #samain dengan nama class