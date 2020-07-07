import discord
from discord.ext import commands
from discord import Embed
import random
import praw
from prawcore import exceptions
from robiconf.bot_configuration import RedditClient
from discord.ext.commands.errors import CommandInvokeError

class Reddit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['r'])
    async def reddit(self, ctx, subreddit_search = "", submission_search = "", *args):
        reddit_client = RedditClient.reddit_client           
        if submission_search != "":
            zero_result = True
            searchword = ""                        
            for n in args:          
                searchword = searchword + " " + n        
            posts = random.choice([x for x in reddit_client.subreddit(subreddit_search).search(submission_search+" "+searchword, limit=20)])            
        else:
            posts = random.choice([x for x in reddit_client.subreddit(subreddit_search).random_rising(limit = 1)])
       
        if posts.thumbnail:
            embedVar = Embed(title=posts.title, url=posts.url)
            embedVar.set_image(url=posts.url)
        else:
            embedVar = Embed(title=posts.title, url=posts.url)
        await ctx.channel.send(embed = embedVar)
        if not posts.thumbnail and not posts.selftext == '': await ctx.channel.send(f' >>> {posts.selftext}')
            

    @reddit.error
    async def reddit_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.channel.send('Kesalahan Penggunan Command.\n > !reddit <namasubreddit> <optional:submissionsearch>')        

        if isinstance(error, exceptions.Redirect):
            await ctx.channel.send('Subreddit Gagal Ditemukan atau Tidak Tersedia')

        if isinstance(error, CommandInvokeError):
            await ctx.channel.send('Submission Gagal Ditemukan atau Tidak Tersedia')

        raise error

def setup(bot):
    bot.add_cog(Reddit(bot))