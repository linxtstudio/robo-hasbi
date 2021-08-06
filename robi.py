import os
import robi_request
from webhooks import loker
import base64
from configuration import BotInstance
from threading import Thread
from discord_message_components import Extension

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
  if filename.endswith('.py') and not (filename[:-3] == "misc" or filename[:-3] == "settings"):
    bot.load_extension(f'cogs.{filename[:-3]}')

@bot.event
async def on_ready():
  extension = Extension(bot)
  channel = bot.get_channel(727873186951200770)
  await channel.send('maaf tadi ketiduran')
  print(f'{bot.user} has connected to Discord!')
  
robi_request.wakeup()
Thread(target=loker.cari_loker).start()
bot.run(token_utf8.decode('utf-8'), bot=True, reconnect=True)
