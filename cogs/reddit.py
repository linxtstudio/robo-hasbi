from asyncio import TimeoutError
from asyncprawcore.exceptions import Redirect, ServerError
from discord import Embed
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

    @reddit.error
    async def reddit_error(self, ctx, error):
        embed = Embed(color=0xff0000, title='Terjadi Kesalahan Saat Menjalankan Command Reddit')
        error = error.original if hasattr(error, 'original') else error

        if isinstance(error, commands.MissingRequiredArgument):
            embed.add_field(name='\u200b', value='Kesalahan Penggunan Command.\n > !reddit <namasubreddit> <optional:submissionsearch>')

        if isinstance(error, Redirect):
            embed.add_field(name='\u200b', value='Subreddit Gagal Ditemukan atau Tidak Tersedia')

        if isinstance(error, IndexError):
            embed.add_field(name='\u200b', value='Submission Gagal Ditemukan atau Tidak Tersedia')

        if isinstance(error, ServerError):
            pass

        embed.set_footer(text=error)
        
        return await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Reddit(bot))