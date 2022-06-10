from discord import Embed
from discord.ext.commands import Bot, Context, command, has_any_role, MissingAnyRole
from os import listdir, getenv
from dotenv import load_dotenv
load_dotenv()
import json
import requests

from helpers.ui import UI

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
    return bot.get_channel(data['pinned-gallery-channel'])

def get_bot_dev_channel(bot: Bot):
    data = load_setting_file()
    return bot.get_channel(data['bot-dev-channel'])

def get_anonymous_channel(bot: Bot):
    data = load_setting_file()
    return bot.get_channel(data['anonymous-channel'])

def get_ruang_pribadi_channel(bot: Bot):
    data = load_setting_file()
    return bot.get_channel(data['ruang-pribadi-channel'])

def get_auto_voice_category(bot: Bot):
    data = load_setting_file()
    return bot.get_channel(data['auto-voice-category'])

@command(name='loadall')
async def loadall(ctx: Context):
    async with ctx.typing():
        for filename in listdir('./cogs'):  
            if filename.endswith('.py'):
                try: ctx.bot.load_extension(f'cogs.{filename[:-3]}')
                except: pass
        
    await ctx.send(embed=UI.success_embed("Semua cogs sudah berhasil Dimuat"))

@command(name='unloadall')
async def unloadall(ctx: Context):
    async with ctx.typing():
        for filename in listdir('./cogs'):  
            if filename.endswith('.py'):
                try: ctx.bot.unload_extension(f'cogs.{filename[:-3]}')
                except: pass

    await ctx.send(embed=UI.success_embed("Semua cogs sudah berhasil dilepas"))

@command(name='kampung')
@has_any_role(949976437266464788)
async def kampung(ctx: Context, action):
    async with ctx.typing():
        if action == 'start':
            requests.post('https://api.idcloudhost.com/v1/jkt01/user-resource/vm/start', headers={'apikey': getenv('ID_CLOUD_API_KEY')}, data={'uuid': '4fe69833-9463-48f9-97b4-a194c5cb504e'})
            return await ctx.send(embed=UI.success_embed("Server Berhasil Nyala"))

        if action == 'stop':
            requests.post('https://api.idcloudhost.com/v1/jkt01/user-resource/vm/stop', headers={'apikey': getenv('ID_CLOUD_API_KEY')}, data={'uuid': '4fe69833-9463-48f9-97b4-a194c5cb504e'})
            return await ctx.send(embed=UI.success_embed("Server Berhasil Mati"))

        if action == 'info':
            resp = requests.get('https://api.idcloudhost.com/v1/jkt01/user-resource/vm', headers={'apikey': getenv('ID_CLOUD_API_KEY')}, data={'uuid': '4fe69833-9463-48f9-97b4-a194c5cb504e'})
            return await ctx.send(embed=UI.success_embed(f"Server is {resp.json()['status']}"))

@kampung.error
async def kampung_error(ctx, error):
    embed = Embed(color=0xd62929, title='Terjadi Kesalahan Saat Menjalankan Command Kampung')
    error = error.original if hasattr(error, 'original') else error

    if isinstance(error, MissingAnyRole):
        embed.description = 'Siapa kamu'

    embed.set_footer(text=f'❌  {error}')
    
    return await ctx.send(embed=embed)