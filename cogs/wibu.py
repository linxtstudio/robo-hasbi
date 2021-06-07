from discord.ext import commands
from discord import Embed
import re
from jikanpy import AioJikan

def wibu_404(context: str):
    not_found_embed = Embed(color=0xff0000)
    not_found_embed.add_field(name=f'{context} yang anda cari tidak dapat ditemukan', value='')
    return not_found_embed

def split_eps(song_list: list):
    if len(song_list) <= 1: return song_list
    return [re.split(r'\(([A-Za-z0-9\s-]+){5,}', op)[0] for op in song_list]

class Wibu(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['a', 'kartun'])
    async def anime(self, ctx, *, query: str):
        _jikan = AioJikan()
        async with ctx.typing():
            try:
                search = await _jikan.search(search_type='anime', query=query)
                anime = await _jikan.anime(id=search['results'][0]['mal_id'])

                title = anime['title_english'] + f" ({anime['title_japanese']})" if anime['title_japanese'] and anime['title_english'] else anime['title']
                desc = anime['synopsis'] if len(anime['synopsis']) < 1024 else anime['synopsis'][0:1021]+'...'

                anime_embed = Embed(color=0x00f00, title=title, url=anime['url'])
                anime_embed.set_thumbnail(url=anime['image_url'])
                anime_embed.add_field(name='Sinopsis', value=desc, inline=False)
                anime_embed.add_field(name='Episode', value=anime['episodes'])
                anime_embed.add_field(name='Score', value=anime['score'])
                anime_embed.add_field(name='Ranking', value=anime['rank'])
                anime_embed.add_field(name='Popularity', value=anime['popularity'])
                anime_embed.add_field(name='Rating', value=anime['rating'])
                anime_embed.add_field(name='Aired', value=anime['aired']['string'])

                if anime['genres']:
                    genre_list = [genre['name'] for genre in anime['genres']]
                    genre_inline = ', '.join(genre_list)
                    anime_embed.add_field(name='Genre', value=genre_inline[0:1024], inline=False)

                if anime['opening_themes']:
                    op_list = split_eps([op for op in anime['opening_themes']])
                    op_inline = '\n'.join(op_list)
                    anime_embed.add_field(name='Opening', value=op_inline[0:1024], inline=False)

                if anime['ending_themes']:
                    ed_list = split_eps([ed for ed in anime['ending_themes']])
                    ed_inline = '\n'.join(ed_list)
                    anime_embed.add_field(name='Ending', value=ed_inline[0:1024], inline=False)

                result = await ctx.send(embed=anime_embed)
                result.add_reactions('❗')
                await _jikan.close()
            except:
                await _jikan.close()

def setup(bot):
    bot.add_cog(Wibu(bot))