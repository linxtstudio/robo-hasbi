from discord import Embed
from discord.ext.commands import Bot, Context, command
from os import listdir
import json

def get_max_page(total: int, batch: int):
    max_page = 1
    for index in range(total):
        if (index + 1) % batch == 0:
            max_page += 1

    return max_page

def load_setting_file():
    with open('storage/setting.json') as file:
        return json.load(file)

def get_pinned_galery_channel(bot: Bot):
    data = load_setting_file()
    channel = bot.get_channel(data['pinned-gallery-channel'])
    return channel

def get_bot_dev_channel(bot: Bot):
    data = load_setting_file()
    channel = bot.get_channel(data['bot-dev-channel'])
    return channel

@command(name='loadall')
async def loadall(ctx: Context):
    async with ctx.typing():
        for filename in listdir('./cogs'):  
            if filename.endswith('.py'):
                try: ctx.bot.load_extension(f'cogs.{filename[:-3]}')
                except: pass
        
    await ctx.send(embed=Embed(color=0x00ff00, title='Semua Cogs Sudah Berhasil Dimuat'))

@command(name='unloadall')
async def unloadall(ctx: Context):
    async with ctx.typing():
        for filename in listdir('./cogs'):  
            if filename.endswith('.py'):
                try: ctx.bot.unload_extension(f'cogs.{filename[:-3]}')
                except: pass

    await ctx.send(embed=Embed(color=0x00ff00, title='Semua Cogs Sudah Berhasil Dilepas'))
