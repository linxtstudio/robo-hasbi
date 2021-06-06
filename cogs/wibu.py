from discord.ext import commands
from discord import Embed
from animec.anicore import Anime
from animec.anicore import NotFound404

def wibu_404(context: str):
    not_found_embed = Embed(color=0xff0000)
    not_found_embed.add_field(name=f'{context} yang anda cari tidak dapat ditemukan', value='')
    return not_found_embed

class Wibu(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['a', 'kartun'])
    async def anime(self, ctx, *, query: str):
        try:
            async with ctx.typing():
                anime = Anime(query)
                title = anime.title_english + f" ({anime.title_jp})" if anime.title_jp and anime.title_english else anime.name
                desc = anime.description if len(anime.description) < 1024 else anime.description[0:1021]+"..."

                anime_embed = Embed(color=0x00f00, title=title, url=anime.url)
                anime_embed.set_thumbnail(url=anime.poster)
                anime_embed.add_field(name='Sinopsis', value=desc, inline=False)
                anime_embed.add_field(name='Episode', value=anime.episodes)
                anime_embed.add_field(name='Ranking', value=anime.ranked)
                anime_embed.add_field(name='Aired', value=anime.aired)

                if anime.opening_themes:
                    op_inline = '\n'.join(anime.opening_themes)
                    anime_embed.add_field(name="Opening", value=op_inline, inline=False)

                if anime.ending_themes:
                    ed_inline = '\n'.join(anime.ending_themes)
                    anime_embed.add_field(name="Ending", value=ed_inline, inline=False)

                await ctx.send(embed=anime_embed)
        except NotFound404:
            await ctx.send(embed=wibu_404('Anime'))
            return

def setup(bot):
    bot.add_cog(Wibu(bot))