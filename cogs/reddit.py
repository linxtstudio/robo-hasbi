import random, praw
from discord.ext import commands
from discord import Embed
from prawcore import exceptions
import base64

bot = commands.Bot('!')

class RedditClient:
    id_utf8 = base64.b64decode('bDEyRlBLVndGa2RuQmc=')
    secret_utf8 = base64.b64decode('aGU3UF84RVJ5QWpUTEZ3V2RSQVJyTkhhTDVR')
    username = base64.b64decode('ZGlnaWJpdF9zdHVkaW8=')
    password = base64.b64decode('ZGlnaWJpdDIwMjA=')
    reddit_client = praw.Reddit(
                    client_id=id_utf8.decode('utf-8'),
                    client_secret=secret_utf8.decode('utf-8'),
                    user_agent='Discord Bot (by /u/digibit_studio)',
                    username=username.decode('utf-8'),
                    password=password.decode('utf-8'))

    def __init__(self, client):
        self.client = self.reddit_client

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

        if isinstance(error, commands.CommandInvokeError):
            await ctx.channel.send('Submission Gagal Ditemukan atau Tidak Tersedia')

        if isinstance(error, commands.CommandOnCooldown): 
            await ctx.channel.send('Cooldown boss, coba lagi setelah {:.2f}s'.format(error.retry_after))

        raise error    
        
        
def setup(bot):
    bot.add_cog(Reddit(bot))