from hentai import Hentai, Sort, Format
import discord
from discord.ext import commands
from discord import Embed
from requests.exceptions import HTTPError
import random

def embed_hentai(code):
    try:
        doujin = Hentai(code)
    except HTTPError:
        return Embed(title=f"Doujin dengan code {code} tidak ada")
        
    embed = Embed(title=f"{doujin.title(Format.Pretty)}")
    embed.set_image(url=doujin.thumbnail)        
    embed.add_field(name='Code', value=code)
    for artist in doujin.artist:
        embed.add_field(name='Artist', value=artist.name)  
    embed.add_field(name='Release Date', value=str(doujin.upload_date)[0:10])
    embed.add_field(name="Start Reading", value=doujin.url)
    tags = [tag.name for tag in doujin.tag]
    embed.set_footer(text=f"Tags: {', '.join(tags)}")

    return embed    

class NHentai(commands.Cog):    
    def __init__(self, bot):
        self.bot = bot

    @commands.group(aliases=['doujin'])
    async def hentai(self, ctx):
        if ctx.invoked_subcommand is None and not ctx.subcommand_passed is None:
            await ctx.send('Invalid hentai command passed...')
        elif ctx.invoked_subcommand is None:
            id_ = Hentai.get_random_id()
            embedVar = await ctx.channel.send(embed=embed_hentai(id_))
            await embedVar.add_reaction('❗')
                                
    @hentai.command(aliases=['nuklir', 'id'])                
    async def code(self, ctx, nuclear_code):        
        embedVar = await ctx.channel.send(embed=embed_hentai(nuclear_code))
        await embedVar.add_reaction('❗')

    @hentai.command(aliases=['tags', 'search_tag'])
    async def tag(self, ctx, *, tag_search):
        id_ = random.choice([doujin['id'] for doujin in Hentai.search_by_query(f'tag:{tag_search}', sort=Sort.Popular)])
        embedVar = await ctx.channel.send(embed=embed_hentai(id_))
        await embedVar.add_reaction('❗')

    @hentai.command(aliases=['parodies', 'anime'])                
    async def parody(self, ctx, parodied):
        id_ = random.choice([doujin['id'] for doujin in Hentai.search_by_query(f'parodies:{parodied}', sort=Sort.Popular)])
        embedVar = await ctx.channel.send(embed=embed_hentai(id_))
        await embedVar.add_reaction('❗')

    @hentai.command(aliases=['author', 'writer'])                
    async def artist(self, ctx, artist_name):
        id_ = random.choice([doujin['id'] for doujin in Hentai.search_by_query(f'artist:{artist_name}', sort=Sort.Popular)])
        embedVar = await ctx.channel.send(embed=embed_hentai(id_))
        await embedVar.add_reaction('❗')

    @hentai.command(aliases=['char'])                
    async def character(self, ctx, char_name):
        id_ = random.choice([doujin['id'] for doujin in Hentai.search_by_query(f'character:{char_name}', sort=Sort.Popular)])
        embedVar = await ctx.channel.send(embed=embed_hentai(id_))
        await embedVar.add_reaction('❗')


def setup(bot):
    bot.add_cog(NHentai(bot))