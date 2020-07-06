from discord.ext import commands
from discord import Embed
from discord.ext.commands.errors import CommandInvokeError
import random
from imgurpython import ImgurClient #python imgur api wrapper
import praw #python reddit API wrapper
from prawcore.exceptions import Redirect, NotFound

bot = commands.Bot('!') #prefix

imgur_client = ImgurClient('4db5ce905276402', '7d5187662ae124628c44e4cfdb368a2e13e86167')

reddit_client = praw.Reddit(client_id="l12FPKVwFkdnBg",
                     client_secret="he7P_8ERyAjTLFwWdRARrNHaL5Q",
                     user_agent="Discord Bot (by /u/digibit_studio)",
                     username="digibit_studio",
                     password="digibit2020")

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
  kode = ""
  while i < 6:
    if i == 0: kode += str(random.randint(1,2))
    else: kode += str(random.randint(0,9))
    i += 1
  await ctx.channel.send(kode)

@bot.command(aliases = ['image', 'imgur', 'pict']) 
async def gambar(ctx, search_query = ""):
  if search_query != "":
    images = imgur_client.gallery_search(search_query, advanced=None, sort='viral', window='all', page=0)
    randomResult = random.choice(images)
    embedVar = Embed(title=randomResult.title, url=randomResult.link)
    embedVar.set_image(url=randomResult.link)
    await ctx.channel.send(embed = embedVar)
  else:
    await ctx.channel.send('Kesalahan Penggunan Command.\n > !gambar <keywordgambar>')

@bot.command()
async def reddit(ctx, subreddit_search = "", submission_search = "",*args):
  try:
    if subreddit_search != "":         
      if submission_search != "":    
        searchword = ""  
        zero_result = True  
        for n in args:          
          searchword = searchword + " " + n
        posts = reddit_client.subreddit(subreddit_search).search(submission_search+" "+searchword, limit=1)
      else:
        posts = reddit_client.subreddit(subreddit_search).random_rising(limit = 1)     
      for submission in posts:    
          zero_result = False
          if submission.thumbnail:
            embedVar = Embed(title=submission.title, url=submission.url)
            embedVar.set_image(url=submission.url)
          else:
            embedVar = Embed(title=submission.title, url=submission.url)
          await ctx.channel.send(embed = embedVar)
          if not submission.thumbnail and not submission.selftext == '': await ctx.channel.send(f' >>> {deskripsi}') 
      if zero_result:
        await ctx.channel.send('Submission Gagal Ditemukan atau Tidak Tersedia')
    else:
      await ctx.channel.send('Kesalahan Penggunan Command.\n > !reddit <namasubreddit> <optional:submissionsearch')
  except Redirect:
    await ctx.channel.send('Subreddit Gagal Ditemukan atau Tidak Tersedia')
  except NotFound:
    await ctx.channel.send('Error Response 404')  

bot.run("NzI3ODY2MDUxNTU5MTYxOTM2.XwAXCQ.TwvoeGhGG0o8CRV_BNX5zfE7qH0")