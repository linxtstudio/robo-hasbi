from asyncio import TimeoutError
from discord.ext import commands
from discord.errors import NotFound
from helpers.pixiv_helpers import PixivWrapper
from random import shuffle

class Pixiv(commands.Cog):
    wrapper = PixivWrapper()

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['p'])
    async def pixiv(self, ctx, *, search=''):
        async with ctx.typing():
            self.wrapper.auth()
            if not search:
                illustrations = [tag['illust'] for tag in self.wrapper.client.trending_tags_illust()['trend_tags']]
            else:
                if search.lower() in ['trend', 'trending']:
                    illustrations = self.wrapper.client.illust_ranking(mode='day').illusts
                elif search.lower() in ['r18', 'nsfw']:
                    illustrations = self.wrapper.client.illust_ranking(mode='day_r18').illusts
                else:
                    illustrations = self.wrapper.client.search_illust(word=search, duration='within_last_month', sort='popular_desc').illusts

            shuffle(illustrations)
            page = 1
            max_index = len(illustrations)
            embed, components = self.wrapper.generate_embed(illustrations[page-1], max_index, page)

            pix = await ctx.send(embed=embed, components=components)

        try:
            while True:
                btn = await pix.wait_for('button', self.bot, timeout=60)
                await btn.respond(ninja_mode=True)

                if btn.custom_id == 'pixiv_first': page = 1
                if btn.custom_id == 'pixiv_prev': page -= 1
                if btn.custom_id == 'pixiv_next': page += 1
                if btn.custom_id == 'pixiv_last': page = max_index

                embed, components = self.wrapper.generate_embed(illustrations[page-1], max_index, page)
                await pix.edit(embed=embed, components=components)
        except TimeoutError:
            _, components = self.wrapper.generate_embed(illustrations[page-1], max_index, page, disable_components=True)
            await pix.edit(components=components)
        except NotFound:
            pass

    @commands.command(aliases=['pid'])
    async def pixiv_detail(self, ctx, id):
        illustration = self.wrapper.client.illust_detail(id)['illust']
        embed, components = self.wrapper.generate_embed(illustration, 1, 1)

        await ctx.send(embed=embed, components=components)

def setup(bot):
    bot.add_cog(Pixiv(bot))
