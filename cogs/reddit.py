import discord
from discord.ext import commands
from discord import Embed
import praw
from prawcore.exceptions import Redirect, NotFound
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
                posts = reddit_client.subreddit(subreddit_search).search(submission_search+" "+searchword, limit=1)
        else:
            posts = reddit_client.subreddit(subreddit_search).random_rising(limit = 1)
    
        for submission in posts:    
            zero_result = False
            if submission.thumbnail:
                embedVar = Embed(title=submission.title, url=submission.url)
                embedVar.set_image(url=submission.url)
            else:
                embedVar = Embed(title=submission.title, url=submission.url)
            await ctx.channel.send(embed = embedVar)
            if not submission.thumbnail and not submission.selftext == '': await ctx.channel.send(f' >>> {deskripsi}')
        if zero_result:
            await ctx.channel.send('Submission Gagal Ditemukan atau Tidak Tersedia')
            

    @reddit.error
    async def reddit_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.channel.send('Kesalahan Penggunan Command.\n > !reddit <namasubreddit> <optional:submissionsearch>')        

        if isinstance(error, commands.CommandInvokeError):
            await ctx.channel.send('Subreddit Gagal Ditemukan atau Tidak Tersedia')

        raise error

def setup(bot):
    bot.add_cog(Reddit(bot))