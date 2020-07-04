from discord.ext import commands
import random
from imgurpython import ImgurClient #python imgur api wrapper

bot = commands.Bot('!') #prefix

client = ImgurClient('4db5ce905276402', '7d5187662ae124628c44e4cfdb368a2e13e86167')

@bot.event
async def on_ready():
  print(f'{bot.user} has connected to Discord!')
    
@bot.event
async def on_command_error(ctx, error):
  if isinstance(error, commands.CommandOnCooldown):    
    await ctx.channel.send('Cooldown boss, coba lagi setelah {:.2f}s'.format(error.retry_after))
  raise error

@bot.command(aliases = ['who', 'saha']) #alias untuk command (pake prefix)
async def siapa(ctx): #nama command (harus dipanggil pakai prefix diatas)  
  await ctx.channel.send("kamu adalah {}".format(ctx.author.nick))

@bot.command()
async def ping(ctx):
  await ctx.channel.send(f'{round(bot.latency*1000)}ms')

@bot.command()
@commands.cooldown(1, 5)
async def code(ctx):
  i = 0
  kode: str
  while i < 6:
    if i == 0: kode += str(random.randint(1,2))
    else: kode += str(random.randint(0,9))
    i += 1
  await ctx.channel.send(kode)

@bot.command(aliases = ['image', 'imgur', 'pict']) 
async def gambar(ctx, search_query = ""):
  images = client.gallery_search(search_query, advanced=None, sort='time', window='all', page=0)
  random_result = random.choice(images)
  image_title = random_result.title if random_result.title else 'Untitled'
  await ctx.channel.send('{0}\n{1}'.format(image_title, random_result.link))

bot.run("NzI3ODY2MDUxNTU5MTYxOTM2.XwAXCQ.TwvoeGhGG0o8CRV_BNX5zfE7qH0")