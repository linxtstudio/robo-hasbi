from discord.ext import commands
import random

bot = commands.Bot('!') #prefix

@bot.event
async def on_ready():
  print(f'{bot.user} has connected to Discord!')
    
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
      message = ctx.channel
      await message.send('Cooldown boss, coba lagi setelah {:.2f}s'.format(error.retry_after))
    raise error

@bot.command(aliases = ['who', 'saha']) #alias untuk command (pake prefix)
async def siapa(ctx): #nama command (harus dipanggil pakai prefix diatas)
  message = ctx.channel
  await message.send("kamu adalah {}".format(ctx.author.nick))

@bot.command()
async def ping(ctx):
  await ctx.channel.send(f'{round(bot.latency*1000)}ms')

@bot.command()
@commands.cooldown(1, 5)
async def code(ctx):
  i = 0
  kode = ''
  while i < 6:
    if i == 0:
      kode += str(random.randint(1,2))
    else:
      kode += str(random.randint(0,9))
    i += 1

  message = ctx.channel
  await message.send(kode)
    
@bot.command()
async def Jojo(ctx):
    img = ["https://images3.alphacoders.com/755/thumb-1920-755384.png", "https://images5.alphacoders.com/433/thumb-1920-433569.jpg", "https://images6.alphacoders.com/833/thumb-1920-833684.png", "https://images4.alphacoders.com/828/thumb-1920-828658.png"]
    message = ctx.channel
    await message.send(random.choice(img))


bot.run("NzI3ODY2MDUxNTU5MTYxOTM2.XvyHYg.vxxKbFe1QnCniBhNMkODispYla0")