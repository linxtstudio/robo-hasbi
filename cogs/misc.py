import discord
import random
from discord.ext import commands
from configuration import BotInstance
from robiconf.bot_configuration import connectDB

cursor = connectDB.db.cursor()

bot = BotInstance.bot #ngambil instance bot dari robiconf biar samaan sama robi.py

class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases = ['who', 'saha']) 
    async def siapa(self, ctx, user: discord.Member): #nama command (harus dipanggil pakai prefix diatas)
        record = getData(user)[0]
        if record == 0 or getData(user)[1] == None: await ctx.channel.send("{} adalah {}".format(user.mention, user.nick))
        else: await ctx.channel.send("{} adalah {}".format(user.mention, getData(user)[1]))

    @siapa.error
    async def siapa_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            getData(ctx.author)
            record = getData(ctx.author)[0]
            if record == 0: await ctx.channel.send("{} adalah {}".format(ctx.author.mention, ctx.author.nick))
            else: await ctx.channel.send("{} adalah {}".format(ctx.author.mention, getData(ctx.author)[1]))

        raise error

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

def getData(user: discord.Member):
    userID = str(user.id)
    sql = "SELECT count(name), name FROM data where id='"+userID+"'"
    cursor.execute(sql)
    results = cursor.fetchone()
    return results

def setup(bot):
    bot.add_cog(Misc(bot))