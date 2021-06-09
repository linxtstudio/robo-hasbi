from discord.ext import commands
from discord import Embed
import re
from jikanpy import AioJikan
from jikanpy.exceptions import APIException

def wibu_404(context: str):
    not_found_embed = Embed(color=0xff0000)
    not_found_embed.add_field(name=f'{context} yang anda cari tidak dapat ditemukan', value='Sad')
    return not_found_embed

def split_eps(song_list: list):
    if len(song_list) <= 1: return song_list
    return [re.split(r'\(([A-Za-z0-9\s-]+){5,}', op)[0] for op in song_list]

def clean(text: str):
    text = text if not text.__contains__(r'\n') else text.replace(r'\n', '')
    text = text if not text.__contains__(r'\t') else text.replace(r'\t', '')
    text = text if not text.__contains__(r'\r') else text.replace(r'\r', '')
    return text

class Wibu(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['a', 'kartun'])
    async def anime(self, ctx, *, query: str):
        _jikan = AioJikan()
        while len(query) < 3: query += ' '

        async with ctx.typing():
            try:
                search = await _jikan.search(search_type='anime', query=query)
                anime = await _jikan.anime(id=search['results'][0]['mal_id'])

                title = anime['title_english'] + f" ({anime['title_japanese']})" if anime['title_japanese'] and anime['title_english'] else anime['title']
                desc = anime['synopsis'] if anime['synopsis'] and len(anime['synopsis']) < 1024 else anime['synopsis'][0:1021]+'...'
                rank = '#'+str(anime['rank'])
                popularity = '#'+str(anime['popularity'])
                genres = ', '.join([genre['name'] for genre in anime['genres']])

                anime_embed = Embed(color=0x00f00, title=title, url=anime['url'])
                anime_embed.set_thumbnail(url=anime['image_url'])
                anime_embed.add_field(name='Synopsis', value=desc, inline=False)
                anime_embed.add_field(name='Episode', value=anime['episodes'])
                anime_embed.add_field(name='Score', value=anime['score'])
                anime_embed.add_field(name='Ranking', value=rank)
                anime_embed.add_field(name='Popularity', value=popularity)
                anime_embed.add_field(name='Rating', value=anime['rating'])
                anime_embed.add_field(name='Aired', value=anime['aired']['string'])
                anime_embed.add_field(name='Genre', value=genres, inline=False)

                if anime['opening_themes']:
                    op_list = split_eps([op for op in anime['opening_themes']])
                    op_inline = '\n'.join(op_list)
                    anime_embed.add_field(name='Opening', value=op_inline[0:1024], inline=False)

                if anime['ending_themes']:
                    ed_list = split_eps([ed for ed in anime['ending_themes']])
                    ed_inline = '\n'.join(ed_list)
                    anime_embed.add_field(name='Ending', value=ed_inline[0:1024], inline=False)

                result = await ctx.send(embed=anime_embed)
            except APIException:
                result = await ctx.send(embed=wibu_404('Anime'))
            finally:
                await result.add_reaction('❗')
                await _jikan.close()
        
    @commands.command(aliases=['c', 'char'])
    async def character(self, ctx, *, query: str):
        _jikan = AioJikan()
        while len(query) < 3: query += ' '

        try:
            async with ctx.typing():
                search = await _jikan.search(search_type='character', query=query)
                char = await _jikan.character(search['results'][0]['mal_id'])
                
                title = char['name'] + f" ({', '.join(char['nicknames'])})" if char['nicknames'] else char['name']
                about = clean(char['about'])
                about = about if len(about) < 1024 else about[0:1021]+'...'
                anime = '\n'.join([role['name']+f" ({role['role']})" for role in char['animeography']]) if char['animeography'] else '-'
                manga = '\n'.join([role['name']+f" ({role['role']})" for role in char['mangaography']]) if char['mangaography'] else '-'
                seiyuu = '\n'.join([person['name']+f" ({person['language']})" for person in char['voice_actors']]) if char['voice_actors'] else '-'

                char_embed = Embed(color=0x00ff00, title=title, url=char['url'])
                char_embed.set_image(url=char['image_url'])
                char_embed.add_field(name='About', value=about, inline=False)
                char_embed.add_field(name='Anime', value=anime[0:1024], inline=False)
                char_embed.add_field(name='Manga', value=manga[0:1024], inline=False)
                char_embed.add_field(name='Seiyuu', value=seiyuu, inline=False)

                result = await ctx.send(embed=char_embed)
        except APIException:
            result = await ctx.send(embed=wibu_404('Karakter'))
        finally:
            await result.add_reaction('❗')
            await _jikan.close()

    @commands.command(aliases=['m',])
    async def manga(self, ctx, *, query: str):
        _jikan = AioJikan()
        while len(query) < 3: query += ' '

        try:
            async with ctx.typing():
                search = await _jikan.search(search_type='manga', query=query)
                manga = await _jikan.manga(search['results'][0]['mal_id'])
                
                title = manga['title'] + f" ({manga['title_japanese']})" if manga['title_japanese'] else manga['title']
                synopsis = manga['synopsis'] if manga['synopsis'] and len(manga['synopsis']) < 1024 else manga['synopsis'][0:1021]+'...'
                rank = '#'+str(manga['rank'])
                popularity = '#'+str(manga['popularity'])
                genres = ', '.join([genre['name'] for genre in manga['genres']])

                manga_embed = Embed(title=title, url=manga['url'])
                manga_embed.set_thumbnail(url=manga['image_url'])
                manga_embed.add_field(name='Synopsis', value=synopsis, inline=False)
                manga_embed.add_field(name='Status', value=manga['status'])
                manga_embed.add_field(name='Total Volumes' if manga['status'] == 'Finished' else 'Latest Volume', value=manga['volumes'])
                manga_embed.add_field(name='Total Chapters' if manga['status'] == 'Finished' else 'Latest Chapter', value=manga['chapters'])
                manga_embed.add_field(name='Score', value=manga['score'])
                manga_embed.add_field(name='Ranking', value=rank)
                manga_embed.add_field(name='Popularity', value=popularity)
                manga_embed.add_field(name='Genre', value=genres, inline=False)

                result = await ctx.send(embed=manga_embed)
        except APIException:
            result = await ctx.send(embed=wibu_404('Manga'))
        finally:
            await result.add_reaction('❗')
            await _jikan.close()

def setup(bot):
    bot.add_cog(Wibu(bot))