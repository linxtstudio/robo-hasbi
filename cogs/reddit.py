import random, praw
from discord.ext import commands
from discord import Embed
from prawcore import exceptions
import base64
from discord_message_components import Button
import asyncio

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

def search_submission(reddit_client, subreddit_search, submission_search, sort, time_filter):
    if submission_search != "":      
        return random.choice([x for x in reddit_client.subreddit(subreddit_search).search(
            query=submission_search,
            sort=sort,
            time_filter=time_filter,
            limit=100)])

    return random.choice([x for x in reddit_client.subreddit(subreddit_search).hot(limit=100)])

def check_is_imgur(url):
  if url.__contains__("/a/"):
      url = url.replace("/a", "")
  if url.__contains__("https://imgur.com") or url.__contains__("http://imgur.com"):
      url = url.replace("imgur.com", "i.imgur.com")
      url += ".jpg"

  return url, url.__contains__("imgur.com")

def sort_check(search):
    valid_sort = [
      'sort:new',
      'sort:relevance',
      'sort:hot',
      'sort:top',
      'sort:comments',
    ]

    if 'sort:' in search:
        for sort in valid_sort:
            if search.__contains__(str(sort)):
                search = search.replace(str(sort), "")
                return str(sort)[5:], search

        search = search.replace('sort:', '')
        return 'invalid', search

    return 'relevance', search

def time_check(search):
    valid_time = [
      'time:all',
      'time:day',
      'time:hour',
      'time:month',
      'time:week',
      'time:year',
    ]
    if 'time:' in search:
        for times in valid_time:
            if search.__contains__(str(times)):
                search = search.replace(times, "")
                return times[5:], search

        search = search.replace('time:', '')
        return 'invalid', search
    
    return 'all', search

from datetime import datetime

def utc_to_local(utc):
    return datetime.utcfromtimestamp(utc).strftime('%Y-%m-%d %H:%M:%S')

class Reddit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_post(self, subreddit_search, submission_search, reddit_client):
        nsfw = nsfw_check(submission_search)
        sort, submission_search = sort_check(submission_search)
        time_filter, submission_search = time_check(submission_search)
        posts = search_submission(reddit_client, subreddit_search, submission_search, sort, time_filter)
        
        iteration = 0
        posts.url, imgur = check_is_imgur(posts.url)

        while nsfw and not posts.over_18:
            if iteration >= 10: raise commands.CommandInvokeError
            posts = search_submission(reddit_client, subreddit_search, submission_search)
            iteration += 1

        embedVar = Embed(title=posts.title, url=posts.url)
        embedVar.set_author(name=f'Post by /u/{posts.author}', url=f'https://www.reddit.com/user/{posts.author}')

        if posts.link_flair_text:
            embedVar.add_field(name='Flair', value=f"{posts.link_flair_text}", inline=True)

        if posts.over_18:
            embedVar.add_field(name='Marked', value="NSFW", inline=True)

        embedVar.add_field(name='Posted On', value=utc_to_local(posts.created_utc))
        
        if posts.thumbnail and (check_is_valid_image(posts.url) or imgur):
            embedVar.set_image(url=posts.url)

        if posts.is_video:
            embedVar.set_video(video=posts.url)

        if posts.selftext != '' and len(str(posts.selftext)) <= 1024:
            embedVar.add_field(name='\u200b', value=posts.selftext, inline=False)

        embedVar.set_footer(text=f'👍 {posts.ups} | 👎 {posts.downs}')
        return embedVar

    @commands.command(aliases=['r'])
    async def reddit(self, ctx, subreddit_search, *, submission_search=""):
        async with ctx.typing():
            reddit_client = RedditClient.reddit_client
            reddit = await ctx.channel.send(
                embed = self.get_post(subreddit_search, submission_search, reddit_client),
                components = [
                    Button('reinvoke', 'Search Ini Lagi', 'green'),
                    Button('delete', 'Delete', 'red')
                ])
          
        try:
            while True:
                btn = await reddit.wait_for(self.bot, 'button', timeout=60)
                await btn.respond(ninja_mode=True)

                if btn.custom_id == 'reinvoke':
                    await reddit.edit(
                        embed = self.get_post(subreddit_search, submission_search, reddit_client),
                        components = [
                            Button('reinvoke', 'Search Ini Lagi', 'green'),
                            Button('delete', 'Delete', 'red')
                        ])
        except asyncio.TimeoutError:
            await reddit.edit(
                components = [
                    Button('reinvoke', 'Search Ini Lagi', 'green', disabled=True),
                    Button('delete', 'Delete', 'red', disabled=False)
                ])

    @reddit.error
    async def reddit_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.channel.send('Kesalahan Penggunan Command.\n > !reddit <namasubreddit> <optional:submissionsearch>')        

        if isinstance(error, exceptions.Redirect):
            await ctx.channel.send('Subreddit Gagal Ditemukan atau Tidak Tersedia')

        if isinstance(error, commands.CommandInvokeError):
            if isinstance(error.original, exceptions.Redirect) or isinstance(error.original, IndexError):
                await ctx.channel.send(embed=Embed(title='Submission Gagal Ditemukan atau Tidak Tersedia', color=0xff0000))

        if isinstance(error, commands.CommandOnCooldown): 
            await ctx.channel.send('Cooldown boss, coba lagi setelah {:.2f}s'.format(error.retry_after))

        if isinstance(error, exceptions.ServerError):
            pass

        raise error    
        
        
def setup(bot):
    bot.add_cog(Reddit(bot))