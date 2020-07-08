import discord
from discord.ext import commands

class Event(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):    
            await ctx.channel.send('Cooldown boss, coba lagi setelah {:.2f}s'.format(error.retry_after)) 
             
        if isinstance(error, commands.CommandNotFound):
            await ctx.channel.send('Gaada command itu, ketik !help untuk melihat daftar lengkap command')      

        raise error

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):  
        if reaction.emoji == '❗' and not user.name == 'Robo-Hasbi' and reaction.message.author.name == 'Robo-Hasbi':
            await reaction.message.delete()

def setup(bot):
    bot.add_cog(Event(bot))