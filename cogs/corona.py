import discord
from discord.ext import commands
from discord import Embed
import requests

class Corona(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.group(aliases=['covid'])
    async def corona(self, ctx):
        if ctx.invoked_subcommand is None and not ctx.subcommand_passed is None:
            await ctx.send('Invalid corona command passed...')
        elif ctx.invoked_subcommand is None:
            positif = requests.get('https://api.kawalcorona.com/positif').json()
            sembuh = requests.get('https://api.kawalcorona.com/sembuh').json()
            meninggal = requests.get('https://api.kawalcorona.com/meninggal').json()
            embedVar = Embed(title=f"Kasus COVID-19 Di Dunia")
            embedVar.add_field(name='Positif', value=positif['value'])
            embedVar.add_field(name='Sembuh', value=sembuh['value'])
            embedVar.add_field(name='Meninggal', value=meninggal['value'])
            embedVar.set_footer(text='Stay safe lakukan protokol COVID-19, ingatlah Hasbi care padamu')
            await ctx.channel.send(embed=embedVar)

    @corona.command(aliases=['country', 'region'])
    async def negara(self, ctx, *, country=''):
        if country == '':
            data = requests.get('https://api.kawalcorona.com/').json()
            embedVar = Embed(title="List Negara (Selain Indonesia)")
            for data in data:
                country_response = data['attributes']
                embedVar.add_field(name=f"ID: {country_response['OBJECTID']}", value=country_response['Country_Region'])
            embedVar.set_footer(text='Stay safe lakukan protokol COVID-19, ingatlah Hasbi care padamu')
            await ctx.channel.send(embed=embedVar)
        else:
            data = requests.get('https://api.kawalcorona.com/').json()
            is_country = False
            for data in data:
                list_data = data['attributes']
                if country.upper() in list_data['Country_Region'].upper() or str(country) in str(list_data['OBJECTID']):
                    embedVar = Embed(title=f"Kasus COVID-19 Di Negara {list_data['Country_Region']}")
                    embedVar.add_field(name='Positif', value=list_data['Confirmed'])
                    embedVar.add_field(name='Sembuh', value=list_data['Recovered'])
                    embedVar.add_field(name='Meninggal', value=list_data['Deaths'])
                    embedVar.set_footer(text='Stay safe lakukan protokol COVID-19, ingatlah Hasbi care padamu')
                    await ctx.channel.send(embed=embedVar)
                    is_country = True
                    break
            if not is_country:                      
                await ctx.channel.send('Tidak ada negara itu dalam list kami\n```!corona negara```')

    @corona.command(aliases=['indo'])
    async def indonesia(self, ctx, provinsi=''):
        if provinsi == '':
            data = requests.get('https://api.kawalcorona.com/indonesia').json()
            embedVar = Embed(title="Kasus COVID-19 Di Indonesia")
            for data in data:
                embedVar.add_field(name='Positif', value=data['positif'])
                embedVar.add_field(name='Sembuh', value=data['sembuh'])
                embedVar.add_field(name='Meninggal', value=data['meninggal'])
                embedVar.add_field(name='Dirawat', value=data['dirawat'])
            embedVar.set_footer(text='Stay safe lakukan protokol COVID-19, ingatlah Hasbi care padamu')
            await ctx.channel.send(embed=embedVar)

        elif provinsi == 'list':
            data = requests.get('https://api.kawalcorona.com/indonesia/provinsi').json()
            embedVar = Embed(title="List Provinsi Di Indonesia")
            for data in data:
                region = data['attributes']
                embedVar.add_field(name=f"ID: {region['Kode_Provi']}", value=region['Provinsi'])
            embedVar.set_footer(text='Stay safe lakukan protokol COVID-19, ingatlah Hasbi care padamu')
            await ctx.channel.send(embed=embedVar)
            
        else:
            data = requests.get('https://api.kawalcorona.com/indonesia/provinsi').json()
            is_provinsi = False 
            for data in data:
                list_data = data['attributes']
                if provinsi.upper() in list_data['Provinsi'].upper() or str(provinsi) in str(list_data['Kode_Provi']):
                    embedVar = Embed(title=f"Kasus COVID-19 Di Indonesia Provinsi {list_data['Provinsi']}")
                    embedVar.add_field(name='Positif', value=list_data['Kasus_Posi'])
                    embedVar.add_field(name='Sembuh', value=list_data['Kasus_Semb'])
                    embedVar.add_field(name='Meninggal', value=list_data['Kasus_Meni'])
                    embedVar.set_footer(text='Stay safe lakukan protokol COVID-19, ingatlah Hasbi care padamu')
                    await ctx.channel.send(embed=embedVar)
                    is_provinsi = True                    
            if not is_provinsi:                      
                await ctx.channel.send('Tidak ada provinsi itu dalam list kami\n```!corona indo list```')

def setup(bot):
    bot.add_cog(Corona(bot))