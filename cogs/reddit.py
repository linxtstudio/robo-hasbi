import random, asyncio, praw, discord
from discord.ext import commands
from discord import Embed, Message
from prawcore import exceptions
from robiconf.bot_configuration import RedditClient, BotInstance
from discord.ext.commands.errors import CommandInvokeError

bot = BotInstance.bot
class Reddit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['r'])
    async def reddit(self, ctx, subreddit_search, *, submission_search=""):        
        reddit_client = RedditClient.reddit_client           
        if submission_search != "":           
            posts = random.choice([x for x in reddit_client.subreddit(subreddit_search).search(submission_search, limit=20)])            
        else:
            posts = random.choice([x for x in reddit_client.subreddit(subreddit_search).random_rising(limit = 1)])
       
        embedVar = Embed(title=posts.title, url=posts.url)
        if posts.thumbnail and posts.is_reddit_media_domain:
            embedVar.add_field(name=f'Post by /u/{posts.author}', value="\u200b")
            if posts.is_video:
                embedVar.set_video(video=posts.url)
            else:
                embedVar.set_image(url=posts.url)
        else:
            if posts.selftext != '' and len(str(posts.selftext)) <= 1024:
                embedVar.add_field(name=f'Post by /u/{posts.author}', value=posts.selftext)

        embedVar.set_footer(text=f'👍 {posts.ups} | 👎 {posts.downs}')
        embed_result = await ctx.channel.send(embed = embedVar)                
        await embed_result.add_reaction('❗')     

    @reddit.error
    async def reddit_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.channel.send('Kesalahan Penggunan Command.\n > !reddit <namasubreddit> <optional:submissionsearch>')        

        if isinstance(error, exceptions.Redirect):
            await ctx.channel.send('Subreddit Gagal Ditemukan atau Tidak Tersedia')

        if isinstance(error, CommandInvokeError):
            await ctx.channel.send('Submission Gagal Ditemukan atau Tidak Tersedia')

        if isinstance(error, commands.CommandOnCooldown): 
            await ctx.channel.send('Cooldown boss, coba lagi setelah {:.2f}s'.format(error.retry_after))

        raise error    
        
        
def setup(bot):
    bot.add_cog(Reddit(bot))