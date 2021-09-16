from hentai import Hentai, Sort, Format
import discord
from discord.ext import commands
from discord import Embed
from requests.exceptions import HTTPError
from functools import wraps
import random

def embed_hentai(code):
    try:
        doujin = Hentai(code)
    except HTTPError:
        return Embed(title=f"Doujin dengan code {code} tidak ada")
      
    
    tags = [tag.name for tag in doujin.tag]
    artists = [artist.name for artist in doujin.artist]
    languages = [language.name for language in doujin.language]
    

    embed = Embed(title=f"{doujin.title(Format.Pretty)}")
    embed.set_image(url=doujin.thumbnail)        
    embed.add_field(name='Code', value=code)
    embed.add_field(name='Artist', value=', '.join(artists))
    embed.add_field(name='Release Date', value=str(doujin.upload_date)[0:10])
    embed.add_field(name='Language', value=', '.join(languages))
    embed.add_field(name='Pages Number', value=doujin.num_pages)
    embed.add_field(name="Start Reading", value=doujin.url)
    
    embed.set_footer(text=f"Tags: {', '.join(tags)}")
    
    return embed

class NHentai(commands.Cog):    
    def __init__(self, bot):
        self.bot = bot

    @commands.group(aliases=['doujin'])
    # @channel_permission
    async def hentai(self, ctx):
        if ctx.invoked_subcommand is None and not ctx.subcommand_passed is None:
            await ctx.send('Invalid hentai command passed...')
        elif ctx.invoked_subcommand is None:
            id_ = Hentai.get_random_id()
            embedVar = await ctx.channel.send(embed=embed_hentai(id_))
            await embedVar.add_reaction('❗')
                                
    @hentai.command(aliases=['nuklir', 'id'])
    # @channel_permission
    async def code(self, ctx, nuclear_code):        
        embedVar = await ctx.channel.send(embed=embed_hentai(nuclear_code))
        await embedVar.add_reaction('❗')

    @hentai.command(aliases=['tags', 'search_tag'])
    # @channel_permission
    async def tag(self, ctx, *, tag_search):
        choices = [doujin['id'] for doujin in Hentai.search_by_query(f'{tag_search}', sort=Sort.Popular)]
        if choices:
            embedVar = await ctx.channel.send(embed=embed_hentai(random.choice(choices)))
        else:
            embedVar = await ctx.channel.send(embed=Embed(title=f"Doujin tidak ada atau tidak dapat ditemukan"))        
        await embedVar.add_reaction('❗')

    @hentai.command(aliases=['parodies', 'anime'])                
    # @channel_permission
    async def parody(self, ctx, *, parodied):
        choices = [doujin['id'] for doujin in Hentai.search_by_query(f'parodies:{parodied}', sort=Sort.Popular)]
        if choices:
            embedVar = await ctx.channel.send(embed=embed_hentai(random.choice(choices)))
        else:
            embedVar = await ctx.channel.send(embed=Embed(title=f"Doujin tidak ada atau tidak dapat ditemukan"))        
        await embedVar.add_reaction('❗')

    @hentai.command(aliases=['author', 'writer'])                
    # @channel_permission
    async def artist(self, ctx, *, artist_name):
        choices = [doujin['id'] for doujin in Hentai.search_by_query(f'artist:{artist_name}', sort=Sort.Popular)]
        if choices:
            embedVar = await ctx.channel.send(embed=embed_hentai(random.choice(choices)))
        else:
            embedVar = await ctx.channel.send(embed=Embed(title=f"Doujin tidak ada atau tidak dapat ditemukan"))        
        await embedVar.add_reaction('❗')

    @hentai.command(aliases=['char'])                
    # @channel_permission
    async def character(self, ctx, *, char_name):
        choices = [doujin['id'] for doujin in Hentai.search_by_query(f'character:{char_name}', sort=Sort.Popular)]
        if choices:
            embedVar = await ctx.channel.send(embed=embed_hentai(random.choice(choices)))
        else:
            embedVar = await ctx.channel.send(embed=Embed(title=f"Doujin tidak ada atau tidak dapat ditemukan"))        
        await embedVar.add_reaction('❗')

    @hentai.command(aliases=['all'])
    # @channel_permission
    async def full(self, ctx, nuclear_code, limit=5):
        doujin = Hentai(nuclear_code)
        pointer = 0
        for image in doujin.image_urls:
            await ctx.channel.send(image)
            pointer += 1
            if pointer > limit: break


def setup(bot):
    bot.add_cog(NHentai(bot))