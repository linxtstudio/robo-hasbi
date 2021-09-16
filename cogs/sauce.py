from asyncio import TimeoutError
from discord.ext import commands
from discord.errors import NotFound
from discord import Embed
from helpers.sauce_helpers import SauceWrapper
from random import shuffle, randint

class Sauce(commands.Cog):
    client = SauceWrapper()

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['s'])
    async def sauce(self, ctx, url: str=''):
        if not url:
            async with ctx.typing():
                lobby = await ctx.send(embed=Embed(color=randint(0, 0xffffff), title='Hasbi menunggu gambar atau link sebelum bisa memberi sauce'))    
            try:
                source = await self.bot.wait_for('message', timeout=60, check=lambda message: message.author == ctx.author)
                url = source.attachments[0].proxy_url if len(source.attachments) > 0 else source.content
            except TimeoutError:
                return await lobby.edit(embed=Embed(color=randint(0, 0xff0000), title='Hasbi lelah menunggu gambar atau link'))

        async with ctx.typing():
            results = await self.client.get_sauce(url)

        if not results:
            return await ctx.send(embed=Embed(color=0xff0000, title='Hasbi tidak menemukan sauce dari gambar tadi mohon maaf'))

        page = 1
        max_index = len(results)
        embed, components = self.client.generate_embed(results[page-1], max_index, page)
        sauce = await ctx.send(embed=embed, components=components)

        try:
            while True:
                btn = await sauce.wait_for('button', self.bot, timeout=60)
                await btn.respond(ninja_mode=True)

                if btn.custom_id == 'sauce_first': page = 1
                if btn.custom_id == 'sauce_prev': page -= 1
                if btn.custom_id == 'sauce_next': page += 1
                if btn.custom_id == 'sauce_last': page = max_index

                embed, components = self.client.generate_embed(results[page-1], max_index, page)
                await sauce.edit(embed=embed, components=components)
        except TimeoutError:
            _, components = self.client.generate_embed(results[page-1], max_index, page, disable_components=True)
            await sauce.edit(components=components)
        except NotFound:
            pass
            

def setup(bot):
    bot.add_cog(Sauce(bot))