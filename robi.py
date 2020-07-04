from discord.ext import commands
import random
from imgurpython import ImgurClient #python imgur api wrapper

bot = commands.Bot('!') #prefix

client = ImgurClient('4db5ce905276402', '7d5187662ae124628c44e4cfdb368a2e13e86167')

@bot.event
async def on_ready():
  print(f'{bot.user} has connected to Discord!')

@bot.command(aliases = ['image', 'imgur', 'pict']) 
async def gambar(ctx, search_query = ""):
  images = client.gallery_search(search_query, advanced=None, sort='time', window='all', page=0)
  random_result = random.choice(images)
  image_title = random_result.title if random_result.title else 'Untitled'
  await ctx.channel.send('{0}\n{1}'.format(image_title, random_result.link))

bot.run("NzI3ODY2MDUxNTU5MTYxOTM2.XwAXCQ.TwvoeGhGG0o8CRV_BNX5zfE7qH0")