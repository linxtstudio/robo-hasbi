import discord
from discord.ext import commands
from discord import Embed
import requests
import re
import asyncio
from configuration import BotInstance

def get_readable_int(amount):
    orig = amount
    new = re.sub("^(-?\d+)(\d{3})", '\g<1>,\g<2>', amount)
    if orig == new:
        return new
    else:
        return get_readable_int(new)

def embed_case(wilayah, positif, sembuh, meninggal, rate):
    embed = Embed(title=f"Kasus COVID-19 Di {wilayah}")
    embed.add_field(name='Positif', value=f'{get_readable_int(positif)}')
    embed.add_field(name='Sembuh', value=get_readable_int(sembuh))
    embed.add_field(name='Meninggal', value=get_readable_int(meninggal))
    embed.add_field(name='Tingkat Kesembuhan', value=f'{rate["recovery_rate"]}%')
    embed.add_field(name='Tingkat Kematian', value=f'{rate["death_rate"]}%')
    embed.set_footer(text='Stay safe lakukan protokol COVID-19, ingatlah Hasbi care padamu')

    return embed

def count_rate(data):
    death_rate = (data['deaths'] / (data['confirmed'] / 100))
    recovery_rate = (data['recovered'] / (data['confirmed'] / 100))

    return {'death_rate': str(death_rate)[0:4], 'recovery_rate': str(recovery_rate)[0:4]}

def embed_countries(batch: int):
    try:
        data = requests.get('https://corona-api.com/countries').json()['data']
        embed = Embed(title=f"List Negara (Page: {batch}/9)")

        for x in range(((batch*25)-25), (batch*25)):
            embed.add_field(name=f"ID: {data[x]['code']}", value=data[x]['name'])
        embed.set_footer(text='Stay safe lakukan protokol COVID-19, ingatlah Hasbi care padamu')

        return embed
    except IndexError:
        embed = Embed(title="Parameter Page Salah")
        return embed

bot = BotInstance.bot

class Corona(commands.Cog):

    def __init__(self, bot):
        self.bot = bot    

    @commands.group(aliases=['covid'])
    async def corona(self, ctx):
        if ctx.invoked_subcommand is None and not ctx.subcommand_passed is None:
            await ctx.send('Invalid corona command passed...')
        elif ctx.invoked_subcommand is None:
            data = requests.get('https://corona-api.com/timeline').json()['data'][0]
            rate = count_rate({'confirmed': data['confirmed'], 'recovered': data['recovered'], 'deaths': data['deaths']})
            await ctx.channel.send(embed=embed_case("Dunia", str(data['confirmed']), str(data['recovered']), str(data['deaths']), rate))

    @corona.command(aliases=['country', 'list'])
    async def negara(self, ctx, page=1):        
        page = page
        countries = await ctx.channel.send(embed=embed_countries(page))

        for emoji in ('⬅️','➡️'):
            await countries.add_reaction(emoji)        

        try:
            while True:
                reaction, user = await bot.wait_for('reaction_add', timeout=60, check=lambda reaction, user: (reaction.emoji == '⬅️' or reaction.emoji == '➡️') and user.name != 'Robo-Hasbi')
                if reaction.emoji == '➡️':
                    if page < 9: page = page + 1
                    await countries.edit(embed=embed_countries(page))
                elif reaction.emoji == '⬅️':
                    if page > 1: page = page - 1
                    await countries.edit(embed=embed_countries(page))
        except asyncio.TimeoutError:
            pass
        

    @corona.command()
    async def id(self, ctx, alphacode: str):
        url = requests.get(f'https://corona-api.com/countries/{alphacode}')
        if url.status_code == 200:            
            data = url.json()['data']
            case = data['latest_data']
            rate = count_rate({'confirmed': case['confirmed'], 'recovered': case['recovered'], 'deaths': case['deaths']})
            await ctx.channel.send(embed=embed_case(data['name'], str(case['confirmed']), str(case['recovered']), str(case['deaths']), rate))
        else:
            embed = Embed(title="Negara dengan ID itu tidak ditemukan")
            await ctx.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Corona(bot))