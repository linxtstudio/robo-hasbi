from discord import Embed
from discord.errors import NotFound
from discord.ext import commands
from hentai import Hentai, Sort, Utils
from hentai.hentai import Format
from helpers.hentai_helpers import NHentaiHelpers
from random import shuffle
from requests.exceptions import HTTPError

class NHentai(commands.Cog):
    helpers = NHentaiHelpers()

    def __init__(self, bot):
        self.bot = bot

    @commands.group(aliases=['h'])
    async def hentai(self, ctx):
        async with ctx.typing():
            if ctx.invoked_subcommand is None:
                await ctx.send(embed=self.helpers.generate_help_embed())

    @hentai.command()
    async def random(self, ctx):
        async with ctx.typing():
            doujin = Utils.get_random_hentai()
            embed, components = self.helpers.generate_list_hentai_embed(doujin, 1, 1, disable_paginator=True)

            await ctx.send(embed=embed, components=components)

    @hentai.command()
    async def search(self, ctx, *, query):
        async with ctx.typing():
            doujins = [doujin for doujin in Utils.search_by_query(query, sort=Sort.Popular)]
            shuffle(doujins)
            curr_index = 1
            max_index = len(doujins)
            embed, components = self.helpers.generate_list_hentai_embed(doujins[curr_index-1], curr_index, max_index)

            nhentai = await ctx.send(embed=embed, components=components)
        
        try:
            while True:
                btn = await nhentai.wait_for('button', self.bot, timeout=60)
                await btn.respond(ninja_mode=True)

                if btn.custom_id == 'hentai_first': curr_index = 1
                if btn.custom_id == 'hentai_prev': curr_index -= 1
                if btn.custom_id == 'hentai_next': curr_index += 1
                if btn.custom_id == 'hentai_last': curr_index = max_index

                embed, components = self.helpers.generate_list_hentai_embed(doujins[curr_index-1], curr_index, max_index)
                await nhentai.edit(embed=embed, components=components)
        except TimeoutError:
            _, components = self.helpers.generate_list_hentai_embed(doujins[curr_index-1], curr_index, max_index, disable_components=True)
            await nhentai.edit(components=components)
        except NotFound:
            pass

    @hentai.command()
    async def read(self, ctx, code):
        async with ctx.typing():
            try:
                doujin = Hentai(code)
            except HTTPError:
                return UI.error_embed(f'Doujin dengan code {code} tidak ada')

            pages = [image for image in doujin.image_urls]
            curr_index = 1
            max_index = len(pages)
            title = doujin.title(Format.Pretty)
            embed, components = self.helpers.generate_read_hentai_embed(title, pages[curr_index-1], curr_index, max_index)

            nhentai = await ctx.send(embed=embed, components=components)
        
        try:
            while True:
                btn = await nhentai.wait_for('button', self.bot, timeout=60)
                await btn.respond(ninja_mode=True)

                if btn.custom_id == 'hentai_first': curr_index = 1
                if btn.custom_id == 'hentai_prev': curr_index -= 1
                if btn.custom_id == 'hentai_next': curr_index += 1
                if btn.custom_id == 'hentai_last': curr_index = max_index

                embed, components = self.helpers.generate_read_hentai_embed(title, pages[curr_index-1], curr_index, max_index)
                await nhentai.edit(embed=embed, components=components)
        except TimeoutError:
            embed, components = self.helpers.generate_read_hentai_embed(title, pages[curr_index-1], curr_index, max_index, disable_components=True)
            await nhentai.edit(components=components)
        except NotFound:
            pass

    @hentai.error
    async def hentai_error(self, ctx, error):
        embed = Embed(color=0xff0000, title='Terjadi Kesalahan Saat Menjalankan Command Hentai')
        error = error.original if hasattr(error, 'original') else error

        if isinstance(error, HTTPError):
            embed.add_field(name='\u200b', value='Doujin Tidak Ditemukan')
            
        embed.set_footer(text=error)
        
        return await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(NHentai(bot))