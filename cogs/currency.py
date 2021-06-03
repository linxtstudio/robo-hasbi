import discord
import random
import time
import requests
import os
from discord.ext import commands
from discord import Embed, Member
from PIL import Image, ImageDraw, ImageFont

class Currency(commands.Cog):
    url_request = "https://robo-hasbi-currency-api.ganiyamustafa.repl.co"
    url_req_pengujian = "http://localhost:5000"
    def __init__(self, bot):
        self.bot = bot

    def get_avatar(self, avatar_url):
        return Image.open(requests.get(avatar_url, stream=True).raw)

    def create_card(self, Id, name, role, avatar_url):
        image = Image.open(f'{os.path.join(os.getcwd())}/idcard/idcard.png')
        pp = self.get_avatar(avatar_url)
        mask = Image.open(f'{os.path.join(os.getcwd())}/idcard/circle.png').convert('L')

        pp = pp.resize(mask.size)
        image.paste(pp, (535,886), mask)

        draw = ImageDraw.Draw(image)

        font = ImageFont.truetype(f'{os.path.join(os.getcwd())}/idcard/Roboto-Bold.ttf', size=75)

        (x, y) = (800, 2690)
        color = 'rgb(0, 0, 0)' # black color
        draw.text((x, y), str(Id), fill=color, font=font)

        (x, y) = (800, 2795)
        color = 'rgb(0, 0, 0)' # black color
        draw.text((x, y), name, fill=color, font=font)

        (x, y) = (800, 2905)
        color = 'rgb(0, 0, 0)' # black color
        draw.text((x, y), role[-1], fill=color, font=font)

        image.save("id_card.png")

    @commands.command(aliases=['regis', 'register'])
    async def reg(self, ctx):
        id_, name = ctx.message.author.id, ctx.message.author.name
        url = f'{self.url_request}/account'
        x = requests.post(url, json={"id": id_, "name": name})
        if x.status_code == 201:
            y = requests.post(f'{self.url_request}/curr/daily', json={"id": id_, 'bal': 0})
            embed = discord.Embed(title="Akun Berhasil Dibuat", color=0x00ff00)
            await ctx.channel.send(embed = embed)
            return
        embed = discord.Embed(title=x.json()['message'], color=0xff0000)
        await ctx.channel.send(embed = embed)

    @commands.command(aliases=['info', 'account'])
    async def account_info(self, ctx, user: discord.Member = None):
        id_ = ctx.message.author.id if not user else user.id
        role = [x.name.upper() for x in ctx.message.author.roles] if not user else [x.name.upper() for x in user.roles]
        avatar_url = ctx.message.author.avatar_url if not user else user.avatar_url
        url = f'{self.url_request}/account'
        x = requests.get(f"{url}/{id_}")

        # with requests.get(ctx.message.author.avatar_url) as r:
        #     img_data = r.content
        # with open('pp.png', 'wb') as handler:
        #     handler.write(img_data)

        if x.status_code == 200:
            name = x.json()['data']['name']
            await ctx.channel.send("Tunggu sebentar, sedang memuat id card")
            self.create_card(id_, name, role, avatar_url)
            with open(f'{os.path.join(os.getcwd())}/id_card.png', 'rb') as f:
                picture = discord.File(f)
                await ctx.channel.send(file=picture)
            os.unlink("id_card.png")
            return
        await ctx.channel.send("User belum terdaftar silahkan regis dulu")

    @commands.command()
    @commands.cooldown(1, 3600*12, commands.BucketType.user) 
    async def daily(self, ctx):
        id_ = ctx.message.author.id
        url = f'{self.url_request}/curr'
        get = requests.get(f'{url}/{id_}')
        bal = 0
        if get.status_code == 200:
            bal = get.json()['data']['bal']
            print(bal)
            x = requests.post(f'{url}/daily', json={'id': id_, 'bal': bal})
            if x.status_code == 200:
                embed = discord.Embed(title=f"{x.json()['curr']} N$ Get", color=0x00ff00)
                await ctx.channel.send(embed = embed)
                return
        embed = discord.Embed(title=f"Anda belum terdaftar silahkan regis dahulu", color=0xff0000)
        await ctx.channel.send(embed = embed)

    @daily.error
    async def daily_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown): 
            cd = time.gmtime(error.retry_after)
            await ctx.channel.send(f'Cooldown boss, coba lagi setelah {time.strftime("%H H %M M %S S",cd)}')

        raise error    

    @commands.command(aliases=["bal"])
    async def ballance(self, ctx, user: discord.Member = None):
        id_ = ctx.message.author.id if not user else user.id
        name = ctx.message.author.name if not user else user.name
        icon = ctx.message.author.avatar_url if not user else user.avatar_url
        url = f'{self.url_request}/curr'
        get = requests.get(f'{url}/{id_}')
        if get.status_code == 200:
            bal = get.json()['data']['bal']
            embed = discord.Embed(color=0x00ff00)
            embed.set_author(name=f"Keuangan {name}", icon_url=icon)
            embed.add_field(name=f"Wallet", value=f"{bal} N$")
            await ctx.channel.send(embed = embed)
            return
        await ctx.channel.send(embed = discord.Embed().add_field(name="Mohon Maaf", value="Sepertinya User Belum Terdaftar Di Dalam Database Kami, Ketik !regis Untuk Mendaftarkan Diri"))

    @commands.group()
    async def shop(self, ctx):
        url = f'{self.url_req_pengujian}/item'
        get = requests.get(url)
        if get.status_code == 200:
            item = get.json()['data']
            embed = discord.Embed(title="Toko Hasbi", color=0x00ff00)
            for x in item:
                embed.add_field(name=f"{x['name']}", value=f"{x['cost']} N$")
            await ctx.channel.send(embed = embed)
            return
        await ctx.channel.send(embed = discord.Embed().add_field(name="Mohon Maaf", value="Sepertinya User Belum Terdaftar Di Dalam Database Kami, Ketik !regis Untuk Mendaftarkan Diri"))

    @shop.command()
    async def item(self, ctx, item):
        url = f'{self.url_req_pengujian}/item/{item}'
        get = requests.get(url)
        if get.status_code == 200:
            item = get.json()['data']
            embed = discord.Embed(title=f"{item['name']}", color=0x00ff00)
            embed.add_field(name=f"{item['cost']} N$", value=f"{item['effect']}")
            await ctx.channel.send(embed = embed)
            return
        await ctx.channel.send(embed = discord.Embed().add_field(name="Mohon Maaf", value="Item tidak tersedia"))

def setup(bot):
    bot.add_cog(Currency(bot))