import discord
from discord.ext import commands
from discord import Embed, Member
from robiconf.bot_configuration import connectDB

cursor = connectDB.db.cursor()

class Settings(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases = ['s', 'set'])
    async def setting(self, ctx, sub1, *sub2):
        name=''
        for n in sub2:
            if(n.lower() == 'reset'): name = ctx.author.nick
            else:
                name += n+' '
                name = name.replace(n[0], n[0].upper(), 1)

        embedVar = Embed(title='Nickname telah diganti menjadi ```'+name+"```", color=0x00ff00)
        try:
            if sub1.lower() == 'profile' or sub1.lower() == 'p':
                if getData(ctx.author)[0] == 0:
                    insertNick(ctx.author.id, name)
                    await ctx.channel.send(embed = embedVar)
                else:
                    updateNick(ctx.author.id, name)
                    await ctx.channel.send(embed = embedVar)
            else: await ctx.channel.send('> error')
        except Exception as e: 
            await ctx.channel.send('> more info `!help setting`')
            print(e)


def getData(user: discord.Member):
        userID = str(user.id)
        sql = "SELECT count(name) FROM data where id='"+userID+"'"
        cursor.execute(sql)
        results = cursor.fetchone()
        return results

def insertNick(id, name):
    sql = "INSERT INTO data (id, name) VALUES (%s, %s)"
    val = (str(id), name)
    cursor.execute(sql, val)
    connectDB.db.commit()

def updateNick(id, name):
    sql = "UPDATE data set name=%s where id=%s"
    val = (name, str(id))
    cursor.execute(sql, val)
    connectDB.db.commit()

def setup(bot):
    bot.add_cog(Settings(bot))