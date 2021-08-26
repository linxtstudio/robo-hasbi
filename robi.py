import os
import robi_request
from webhooks import loker
import base64
from configuration import BotInstance
from threading import Thread
import random
from discord_components import DiscordComponents, Button, ButtonStyle
from discord import Game

bot = BotInstance.bot
token_utf8 = base64.b64decode('TnpJM09EWTJNRFV4TlRVNU1UWXhPVE0yLlh3Tk5BUS5ZSk8wWHlfMHV4MzEyMG5GMURYRml1SVQyLW8=')

@bot.command()
async def load(ctx, extension):
  bot.load_extension(f'cogs.{extension}')
  await ctx.message.add_reaction('👍')
@load.error
async def load_error(ctx, error):
  await ctx.message.add_reaction('👎')

@bot.command()
async def unload(ctx, extension):
  bot.unload_extension(f'cogs.{extension}')
  await ctx.message.add_reaction('👍')
@unload.error
async def unload_error(ctx, error):
  await ctx.message.add_reaction('👎')

@bot.command(aliases=['re'])
async def reload(ctx, extension):
  bot.reload_extension(f'cogs.{extension}')
  await ctx.message.add_reaction('👍')
@reload.error
async def reload_error(ctx, error):
  await ctx.message.add_reaction('👎')

for filename in os.listdir('./cogs'):  
  if filename.endswith('.py'):
    bot.load_extension(f'cogs.{filename[:-3]}')
  # if filename[:-3] in ['sk', 'reddit', 'event']:
  #   bot.load_extension(f'cogs.{filename[:-3]}')

@bot.event
async def on_ready():
  DiscordComponents(bot)
  await bot.change_presence(activity=Game(name='Kampung Pa Yusuf'))
  channel = bot.get_channel(727873186951200770)
  pesan_hasbi = [
    'maaf tadi ketiduran',
    'maaf tadi aku disuruh ke ruang bk dulu',
    'maaf tadi diculik pa ahi naik mobil',
    'maaf tadi aku pipis dulu',
    'maaf baru pulang beli geprek',
    'maaf tadi disadap',
    'maaf tadi dititah pa ahi nyokot buku paket'
  ]
  await channel.send(random.choice(pesan_hasbi))
  print(f'{bot.user} has connected to Discord!')


# Mode Pecinta Naga
history = []
@bot.event
async def on_message(message):
  await bot.process_commands(message)
  gacha = random.choice(range(9))
  repeat = 0

  if message.author.name != 'Robo-Hasbi' and not message.content.startswith('!'):
    if len(message.content.split()) > 10 or len(message.content.lower()) > 50:
      return await message.channel.send('gandeng')

    if 'bi' in message.content.lower() and len(message.content.split()) == 1:
      return await message.channel.send('naon')

    if 'kok' in message.content.lower():
      gacha_kok = random.choice(range(3))
      return await message.channel.send('gpp' if gacha_kok < 1 else 'kok')

    if 'kapan' in message.content.lower():
      return await message.channel.send('kapan kapan')

    if 'atau' in message.content.lower():
      return await message.channel.send('atau')

    if 'gelo' in message.content.lower():
      return await message.channel.send('gelo')

    if 'kah' in message.content.lower() or 'kh' in message.content.lower():
      return await message.channel.send('kh')

    if 'kenapa' in message.content.lower() or 'knp' in message.content.lower():
      return await message.channel.send('gpp')

    if 'malah' in message.content.lower() or 'mlh' in message.content.lower():
      return await message.channel.send('malah')

    if 'bener' in message.content.lower():
      return await message.channel.send('bener euy')

    if len(message.content.split()) == 1:
      history.append(message.content.lower())
      if len(history) > 5:
        history.pop(0)
    
    for word in history:
      if word == message.content.lower(): repeat += 1

    if repeat >= 3:
      return await message.channel.send(message.content.lower())

    if gacha < 3:
      words = message.content.split()
      send_rand = random.choice(words)
      return await message.channel.send(send_rand)

# Start Thread
Thread(target=robi_request.run).start()
Thread(target=loker.cari_loker).start()

# Start The Bot
bot.run(token_utf8.decode('utf-8'), bot=True, reconnect=True)
