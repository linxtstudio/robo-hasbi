import random, praw
from discord.ext import commands
from discord import Embed
from prawcore import exceptions
import base64
from discord_message_components import Button

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

def check_is_valid_image(url):
    url = str(url)
    if url.endswith('jpg') or url.endswith('jpeg') or url.endswith('png') or url.endswith('webm') or url.endswith('gif'):
        return True
    return False
  
def nsfw_check(search_query: str):
    if 'nsfw' in search_query.lower():
        return True
    return False

def search_submission(reddit_client, subreddit_search, submission_search):
    if submission_search != "":           
        return random.choice([x for x in reddit_client.subreddit(subreddit_search).search(submission_search, limit=100)])

    return random.choice([x for x in reddit_client.subreddit(subreddit_search).hot(limit=100)])

def check_is_imgur(url):
  if url.__contains__("/a/"):
      url = url.replace("/a", "")
  if url.__contains__("https://imgur.com") or url.__contains__("http://imgur.com"):
      url = url.replace("imgur.com", "i.imgur.com")
      url += ".jpg"

  return url, url.__contains__("imgur.com")


class Reddit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_post(subreddit_search, submission_search, reddit_client):
        nsfw = nsfw_check(submission_search)
        posts = search_submission(reddit_client, subreddit_search, submission_search)
        iteration = 0
        posts.url, imgur = check_is_imgur(posts.url)

        while nsfw and not posts.over_18:
            if iteration >= 10: raise commands.CommandInvokeError
            posts = search_submission(reddit_client, subreddit_search, submission_search)
            iteration += 1

        embedVar = Embed(title=posts.title, url=posts.url)
        embedVar.set_author(name=f'Post by /u/{posts.author}', url=f'https://www.reddit.com/user/{posts.author}')

        if posts.link_flair_text:
            embedVar.add_field(name='Flair', value=f"{posts.link_flair_text}", inline=False)

        if posts.over_18:
            embedVar.add_field(name='Marked', value="NSFW", inline=False)
        
        if posts.thumbnail and (check_is_valid_image(posts.url) or imgur):
            embedVar.set_image(url=posts.url)

        if posts.is_video:
            embedVar.set_video(video=posts.url)

        if posts.selftext != '' and len(str(posts.selftext)) <= 1024:
            embedVar.add_field(name='\u200b', value=posts.selftext)

        embedVar.set_footer(text=f'👍 {posts.ups} | 👎 {posts.downs}')
        return embedVar

    @commands.command(aliases=['r'])
    async def reddit(self, ctx, subreddit_search, *, submission_search=""):
        async with ctx.typing():
            reddit_client = RedditClient.reddit_client
            reddit = await ctx.channel.send(
                embed = self.get_post(subreddit_search, submission_search, reddit_client),
                components = [
                    Button('reinvoke', 'Search Ini Lagi', 'green', ':mag_right:' )
                ])
            try:
                while True:
                    btn = await reddit.wait_for(self.bot, 'button', timeout=60)
                    await btn.respond(ninja_mode=True)

                    if btn.custom_id == 'reinvoke':
                        reddit.edit(
                            embed = self.get_post(subreddit_search, submission_search, reddit_client),
                            components = [
                                Button('reinvoke', 'Search Ini Lagi', 'green', ':mag_right:' )
                            ])
            except TimeoutError:
                pass            

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