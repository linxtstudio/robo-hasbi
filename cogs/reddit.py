from asyncio import TimeoutError
from discord.ext import commands
from discord.errors import NotFound
from helpers.reddit_helpers import RedditWrapper
from random import shuffle

class Reddit(commands.Cog):
    client = RedditWrapper()

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['r'])
    async def reddit(self, ctx, subreddit, *, search: str=''):
        async with ctx.typing():
            subreddit = await self.client.get_subreddit(subreddit)
            posts = await self.client.get_post(subreddit, search)
            shuffle(posts)
            page = 1
            max_index = len(posts)
            embed, components = self.client.generate_embed(posts[page-1], max_index, page)

            reddit = await ctx.send(embed=embed, components=components)

        try:
            while True:
                btn = await reddit.wait_for('button', self.bot, timeout=60)
                await btn.respond(ninja_mode=True)

                if btn.custom_id == 'reddit_first': page = 1
                if btn.custom_id == 'reddit_prev': page -= 1
                if btn.custom_id == 'reddit_next': page += 1
                if btn.custom_id == 'reddit_last': page = max_index

                embed, components = self.client.generate_embed(posts[page-1], max_index, page)
                await reddit.edit(embed=embed, components=components)
        except TimeoutError:
            _, components = self.client.generate_embed(posts[page-1], max_index, page, disable_components=True)
            await reddit.edit(components=components)
        except NotFound:
            pass


def setup(bot):
    bot.add_cog(Reddit(bot))