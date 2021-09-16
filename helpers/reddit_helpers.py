from asyncpraw import Reddit
from asyncpraw.models import Subreddit, Submission
from base64 import b64decode
from datetime import datetime
from discord import Embed
from discord_ui import Button
from helpers.ui import UI
from random import randint

import re

class RedditWrapper():
    id_ = b64decode('bDEyRlBLVndGa2RuQmc=')
    secret_ = b64decode('aGU3UF84RVJ5QWpUTEZ3V2RSQVJyTkhhTDVR')
    username = b64decode('ZGlnaWJpdF9zdHVkaW8=')
    password = b64decode('ZGlnaWJpdDIwMjA=')
    client = Reddit(
                    client_id=id_.decode('utf-8'),
                    client_secret=secret_.decode('utf-8'),
                    user_agent='Discord Bot (by /u/digibit_studio)',
                    username=username.decode('utf-8'),
                    password=password.decode('utf-8')
                )

    def parse_query(self, query: str):
        query = query.lower()
        holder = {'limit': None, 'sort': None, 'syntax': None, 'time': None}

        for param in ['limit', 'sort', 'syntax', 'time']:
            regex = re.compile(param+r':\s*([^.]+|\S+)', re.IGNORECASE)
            result = regex.search(query)

            holder[param] = result.group(1).split()[0] if result else None
            query = query.replace(f'{param}:{result.group(1).split()[0]}', '') if result else query

        return query, holder['limit'], holder['sort'], holder['syntax'], holder['time']
        
    async def get_subreddit(self, name: str='all'):
        return await self.client.subreddit(name, fetch=True)

    async def get_post(self, subreddit: Subreddit, search_query: str):
        search, limit, sort, syntax, time = self.parse_query(search_query)
        limit = int(limit) if limit else None
        result = []

        if search != '':
            async for submission in subreddit.search(
                query=search,
                sort=sort if sort else 'relevance',
                syntax=syntax if syntax else 'lucene',
                time_filter=time if time else 'all',
                limit=limit if limit else 100): 
                
                result.append(submission)
        else:
            if sort == 'hot':
                result = [submission async for submission in subreddit.hot(limit=limit if limit else 100)]
            elif sort == 'new':
                result = [submission async for submission in subreddit.new(limit=limit if limit else 100)]
            elif sort == 'top':
                result = [submission async for submission in subreddit.top(limit=limit if limit else 100)]
            else:
                result = [submission async for submission in subreddit.random_rising(limit=limit if limit else 100)]

        return result

    def parse_utc(self, utc):
        return datetime.utcfromtimestamp(utc).strftime('%Y-%m-%d')

    def is_valid_image(self, url):
        url = str(url)
        if url.endswith('jpg') or url.endswith('jpeg') or url.endswith('png') or url.endswith('webm') or url.endswith('gif'):
            return True
        return False

    def generate_embed(self, post: Submission, max_index: int, curr_index: int, disable_components: bool=False):
        components = [
            Button(custom_id='reddit_first', color='blurple', emoji=UI.first_arrow, disabled=curr_index==1 or disable_components),
            Button(custom_id='reddit_prev', color='blurple', emoji=UI.previous_arrow, disabled=curr_index==1 or disable_components),
            Button(custom_id='delete', color='red', label='Delete', disabled=False),
            Button(custom_id='reddit_next', color='blurple', emoji=UI.next_arrow, disabled=max_index==1 or (curr_index==max_index) or disable_components),
            Button(custom_id='reddit_last', color='blurple', emoji=UI.last_arrow, disabled=max_index==1 or (curr_index==max_index) or disable_components),
        ]

        embed = Embed(title=post.title[:255], url=post.url, color=randint(0, 0xffffff))
        embed.set_author(name=f'Posted by /u/{post.author} on {self.parse_utc(post.created_utc)}', url=f'https://www.reddit.com/user/{post.author}')

        if post.link_flair_text: embed.add_field(name='Flair', value=f"{post.link_flair_text}", inline=True)
        if post.over_18: embed.add_field(name='Marked', value="NSFW", inline=True)
        if post.thumbnail and self.is_valid_image(post.url):embed.set_image(url=post.url)
        if post.is_video: embed.add_field(name='Video URL', value=post.url, inline=False)
        if post.selftext: embed.add_field(name='\u200b', value=post.selftext[:1024], inline=False)

        embed.set_footer(text=f'👍 {post.ups} | 👎 {post.downs} | {max_index} Posts Found | {curr_index}')

        return embed, components
