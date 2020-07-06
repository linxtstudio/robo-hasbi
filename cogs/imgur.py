import discord
from discord.ext import commands
from discord.ext.commands.errors import CommandInvokeError
from discord import Embed
import random
import imgurpython
from robiconf.bot_configuration import ImgurClient

class Imgur(commands.Cog):    
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases = ['image', 'imgur', 'pict']) 
    async def gambar(self, ctx, keyword_search, *args):
        searchword = ""                        
        for n in args:          
            searchword = searchword + " " + n
        imgur_client = ImgurClient.imgur_client            
        images = imgur_client.gallery_search(keyword_search+' '+searchword, advanced=None, sort='viral', window='all', page=0)
        randomResult = random.choice(images)
        embedVar = Embed(title=randomResult.title, url=randomResult.link)
        embedVar.set_image(url=randomResult.link)
        await ctx.channel.send(embed = embedVar)                
            
    @gambar.error
    async def gambar_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.channel.send('Kesalahan Penggunan Command.\n > !gambar <keywordgambar>')

        if isinstance(error, commands.CommandInvokeError):
            await ctx.channel.send('Terjadi Kesalahan Saat Mencoba Melakukan Koneksi Dengan Imgur')

        raise error

def setup(bot):
    bot.add_cog(Imgur(bot))