import discord
import random
from discord.ext import commands
from discord import Embed, Member
from robiconf.bot_configuration import connectDB

cursor = connectDB.db.cursor()

class Currency(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases = ['d'])
    @commands.cooldown(1, 86400, commands.BucketType.user)
    async def daily(self, ctx):
        bal = random.randint(100,500)
        embedVar = Embed(title="You Get `"+str(bal)+" N$` from daily", color=0x00ff00)
        try:
            if getData(ctx.author)[0] == 0:
                insertCur(ctx.author.id, bal)
                await ctx.channel.send(embed = embedVar)
            else:
                bal = bal+getData(ctx.author)[1]
                bank = getData(ctx.author)[2]
                updateCur(ctx.author.id, bal, bank)
                await ctx.channel.send(embed = embedVar)
        except Exception as e: 
            await ctx.channel.send('> more info `!help currency`')
            print(e)
    
    @commands.command(aliases = ['bal', 'Ballance'])
    async def ballance(self, ctx):
        try:
            if(getData(ctx.author)[0] != 0):
                data = getData(ctx.author)
                wal = data[1]
                bank = data[2]
                tot = wal+bank

                embedVar = Embed(title="Tabunganmmu", 
                                description="**Wallet**: "+str(wal)+" `N$`\n**Bank**: "+str(bank)+" `N$`\n**Total**: "+str(tot)+" `N$`",
                                color=0x00ff00)
            else: embedVar = Embed(title="Your Ballance", 
                                description="**Wallet: **0 `N$`\n**Bank: **0 `N$`\n**Total: **0 `N$`",
                                color=0x00ff00)
            await ctx.channel.send(embed = embedVar)
        except Exception as e: 
            await ctx.channel.send('> more info `!help currency`')
            print(e)

    @commands.command(aliases = ['Deposit'])
    async def deposit(self, ctx, sub1):
        try:
            data = getData(ctx.author)
            if(data[0] == 0): 
                wal = 0
                bank = 0
                depo = 0
            else: 
                if sub1.lower() == 'all':
                    wal = 0
                    bank = data[1]+data[2]
                    depo = str(data[1])
                else:
                    wal = data[1]-int(sub1)
                    bank = data[2]+int(sub1)
                    depo = sub1

            embedVar = Embed(title="Kamu Mendepositkan `"+depo+" N$`", 
                                color=0x00ff00)

            if data[0] == 0 and wal >= 0: insertCur(ctx.author.id, wal, bank)
            elif data[0] != 0 and wal >= 0: updateCur(ctx.author.id, wal, bank)
            else: embedVar = Embed(title="Kamu tidak memiliki jumlah uang yang cukup untuk didepositkan", color=0xFF0000)

            await ctx.channel.send(embed = embedVar)
        except Exception as e: 
            await ctx.channel.send('> more info `!help currency`')
            print(e)
    
    @commands.command(aliases = ['Withdraw'])
    async def withdraw(self, ctx, sub1):
        try:
            data = getData(ctx.author)
            if(data[0] == 0): 
                wal = 0
                bank = 0
                withdraw = 0
            else: 
                if sub1.lower() == 'all':
                    wal = data[1]+data[2]
                    bank = 0
                    withdraw = str(data[2])
                else:
                    wal = data[1]+int(sub1)
                    bank = data[2]-int(sub1)
                    withdraw = sub1
            
            embedVar = Embed(title="Kamu mengambil `"+withdraw+" N$` dari bank", 
                            color=0x00ff00)

            if data[0] == 0 and bank >= 0: insertCur(ctx.author.id, wal, bank)
            elif data[0] != 0 and bank >= 0: updateCur(ctx.author.id, wal, bank)
            else: embedVar = Embed(title="Kamu tidak memiliki jumlah uang yang cukup untuk diambil", color=0xFF0000)

            await ctx.channel.send(embed = embedVar)
        except Exception as e: 
            await ctx.channel.send('> more info `!help currency`')
            print(e)

def getData(user: discord.Member):
        userID = str(user.id)
        sql = "SELECT count(*), ballance, bank FROM currency where idProfil='"+userID+"'"
        cursor.execute(sql)
        results = cursor.fetchone()
        return results

def insertCur(id, bal=None, bank=0):
    sql = "INSERT INTO currency VALUES (%s, %s, %s)"
    val = (str(id), bal, bank)
    cursor.execute(sql, val)
    connectDB.db.commit()

def updateCur(id, bal=None, bank=0):
    sql = "UPDATE currency set ballance=%s, bank=%s where idProfil=%s"
    val = (bal, bank, str(id))
    cursor.execute(sql, val)
    connectDB.db.commit()

def setup(bot):
    bot.add_cog(Currency(bot))