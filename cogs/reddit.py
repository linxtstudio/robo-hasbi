import random, praw
from discord.ext import commands
from discord import Embed
from prawcore import exceptions
import base64
import asyncio
import re
from datetime import datetime
from discord_ui import Button

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

    def sort_check(self, search):
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
            return None, search

        return 'relevance', search

    def time_check(self, search):
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
            return None, search
        
        return 'all', search

    def limit_check(self, search):
        limit = re.search('limit:P(\d+)', search).group(1) if 'limit:' in search else None        
        search = search.replace('limit:', '')
        return limit, search
    
    def is_valid_image(self, url):
        url = str(url)
        if url.endswith('jpg') or url.endswith('jpeg') or url.endswith('png') or url.endswith('webm') or url.endswith('gif'):
            return True
        return False
    
    def nsfw_check(self, search_query):
        if 'nsfw' in search_query.lower():
            return True
        return False

    def check_is_imgur(self, url):
        if url.__contains__("/a/"):
            url = url.replace("/a", "")
        if url.__contains__("https://imgur.com") or url.__contains__("http://imgur.com"):
            url = url.replace("imgur.com", "i.imgur.com")
            url += ".jpg"

        return url, url.__contains__("imgur.com")

    def utc_to_local(self, utc):
        return datetime.utcfromtimestamp(utc).strftime('%Y-%m-%d %H:%M:%S')

    def search_submission(self, reddit_client, subreddit_search, submission_search, sort, time_filter, limit):
        subreddit = reddit_client.subreddit(subreddit_search)
        if submission_search != '':
            posts = subreddit.search(query=submission_search,
                                    sort=sort if sort else 'relevance',
                                    time_filter=time_filter if time_filter else 'all',
                                    limit=limit if limit else 100)
        else:
            posts = subreddit.random_rising(limit=limit if limit else 100)
            if sort == 'hot':
                posts = subreddit.hot(time_filter=time_filter if time_filter else 'all', limit=limit if limit else 100)
            if sort == 'new':
                posts = subreddit.new(time_filter=time_filter if time_filter else 'all', limit=limit if limit else 100)
            if sort == 'top':
                posts = subreddit.top(time_filter=time_filter if time_filter else 'all', limit=limit if limit else 100)

        return [post for post in posts]

    def get_posts(self, subreddit_search, submission_search, reddit_client):
        sort, submission_search = self.sort_check(submission_search)
        time_filter, submission_search = self.time_check(submission_search)
        limit, submission_search = self.limit_check(submission_search)
        posts = self.search_submission(reddit_client, subreddit_search, submission_search, sort, time_filter, limit)

        return posts

    def choose_random(self, posts):
        posts_size = len(posts)

        if posts_size == 0:
            return False, posts

        index = random.choice(range(posts_size))
        post = posts[index]

        del posts[index]
        return post, posts

    def embed_post(self, post, max_result, curr_index):
        post.url, imgur = self.check_is_imgur(post.url)

        embedVar = Embed(title=post.title[:255], url=post.url)
        embedVar.set_author(name=f'Post by /u/{post.author}', url=f'https://www.reddit.com/user/{post.author}')

        if post.link_flair_text:
            embedVar.add_field(name='Flair', value=f"{post.link_flair_text}", inline=True)

        if post.over_18:
            embedVar.add_field(name='Marked', value="NSFW", inline=True)

        embedVar.add_field(name='Posted On', value=self.utc_to_local(post.created_utc))
        
        if post.thumbnail and (self.is_valid_image(post.url) or imgur):
            embedVar.set_image(url=post.url)

        if post.is_video:
            embedVar.set_video(video=post.url)

        if post.selftext != '' and len(str(post.selftext)) <= 1024:
            embedVar.add_field(name='\u200b', value=post.selftext, inline=False)

        embedVar.set_footer(text=f'👍 {post.ups} | 👎 {post.downs} | {max_result} Posts Found | {curr_index}')
        return embedVar

    @commands.command(aliases=['r'])
    async def reddit(self, ctx, subreddit_search, *, submission_search=""):
        async with ctx.typing():
            reddit_client = RedditClient.reddit_client
            posts = self.get_posts(subreddit_search, submission_search, reddit_client)
            max_post = len(posts)
            post, posts = self.choose_random(posts)
            history = [post]
            current_index = 1

            if not post:
                raise IndexError

            reddit = await ctx.channel.send(
                embed = self.embed_post(post, max_post, current_index),
                components = [
                    Button(custom_id='previous', color='blurple', emoji='⬅️', disabled=True),
                    Button(custom_id='delete', label='Delete', color='red'),
                    Button(custom_id='next', color='blurple', emoji='➡️', disabled=False),
                ])
          
        try:
            while True:
                btn = await reddit.wait_for(self.bot, 'button', timeout=60)
                await btn.respond(ninja_mode=True)

                if btn.custom_id == 'next':
                    current_index += 1
                    next_is_last_post = current_index >= max_post
                    research = (max_post != len(history)) and (current_index == len(history)+1)

                    if research:
                        post, posts = self.choose_random(posts)
                        await reddit.edit(
                            embed = self.embed_post(post, max_post, current_index),
                            components = [
                                Button(custom_id='previous', color='blurple', emoji='⬅️', disabled=False),
                                Button('delete', 'Delete', 'red'),
                                Button(custom_id='next', color='blurple', emoji='➡️', disabled=next_is_last_post),
                            ])
                        history.append(post)
                    else:
                        await reddit.edit(
                            embed = self.embed_post(history[current_index-1], max_post, current_index),
                            components = [
                                Button(custom_id='previous', color='blurple', emoji='⬅️', disabled=False),
                                Button('delete', 'Delete', 'red'),
                                Button(custom_id='next', color='blurple', emoji='➡️', disabled=next_is_last_post),
                            ])

                if btn.custom_id == 'previous':
                    current_index -= 1
                    disabled_previous = current_index == 1

                    await reddit.edit(
                        embed = self.embed_post(history[current_index-1], max_post, current_index),
                        components = [
                            Button(custom_id='previous', color='blurple', emoji='⬅️', disabled=disabled_previous),
                            Button('delete', 'Delete', 'red'),
                            Button(custom_id='next', color='blurple', emoji='➡️', disabled=False),
                        ])
            
        except asyncio.TimeoutError:
            await reddit.edit(
                components = [
                    Button(custom_id='previous', color='blurple', emoji='⬅️', disabled=True),
                    Button('delete', 'Delete', 'red', disabled=False),
                    Button(custom_id='next', color='blurple', emoji='➡️', disabled=True),
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