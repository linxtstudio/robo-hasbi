import discord
from discord.ext import commands

class Event(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener() #Default error handler for a command, you can override it if you need a specific error handler
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            cd = int(error.retry_after)
            h = 0
            m = 0
            h = int(cd/3600)
            cd = cd%3600
            if cd != 0 and cd > 60:
                m = int(cd/60)
                cd = cd%60
            
            if str(ctx.command)  == 'daily': await ctx.channel.send('Anda sudah mengambil jatah hari ini, coba lagi setelah `{}h {}m {}s`'.format(h, m, cd)) 
            else: await ctx.channel.send('Cooldown boss, coba lagi setelah {:.2f}s'.format(error.retry_after)) 
             
        if isinstance(error, commands.CommandNotFound):
            await ctx.channel.send('Gaada command itu, ketik !help untuk melihat daftar lengkap command')  

        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.channel.send('Kesalahan Penggunaan Command.\n```!help <namacommand>```')

        if isinstance(error, commands.MissingRole):
            await ctx.channel.send("Kamu gak punya role yang sesuai buat ngejalanin command ini")

        if isinstance(error, commands.MissingAnyRole):
            await ctx.channel.send("Kamu gak punya role yang sesuai buat ngejalanin command ini")

        if isinstance(error, commands.BadArgument):
            await ctx.channel.send("Kesalahan Penggunaan Command.\n```!help <namacommand>```")

        if isinstance(error, commands.CommandInvokeError):
            await ctx.channel.send("Terjadi kesalahan saat mengeksekusi command 😭😭")

        raise error

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user: discord.Member):
        polisi = discord.utils.get(reaction.message.guild.roles, name="Kepolisian")
        tahanan = discord.utils.get(reaction.message.guild.roles, name="Tahanan")
        presiden = discord.utils.get(reaction.message.guild.roles, name="Presiden")
        
        if not user.name == 'Robo-Hasbi' and reaction.message.author.name == 'Robo-Hasbi':            
            if reaction.emoji == '❗':
                await reaction.message.delete()            
                
        # print(f'{user.name} telah mereact {reaction.emoji} \n')

def setup(bot):
    bot.add_cog(Event(bot))