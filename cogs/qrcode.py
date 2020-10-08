import discord
from discord.ext import commands
import os
from MyQR import myqr

class qr_code(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def qr(self, ctx, sub1):
        generate(str(ctx.author.id), sub1)
        with open(os.path.join(os.getcwd(), "src") + "/" + str(ctx.author.id)+".png", 'rb') as f:
            picture = discord.File(f)
            await ctx.channel.send(file=picture)
        
    

def generate(name, subject):
    global qr, photo, filename, save_dir, timestampStr1,type1
    version, level, qr = myqr.run( subject, version=1, level='H', colorized=True, contrast=1.0, brightness=1.0, save_name=name+".png", save_dir=os.path.join(os.getcwd(), "src"))
    type1 = 1

def setup(bot):
    bot.add_cog(qr_code(bot))