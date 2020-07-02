from discord.ext import commands

bot = commands.Bot('!') #prefix

@bot.event
async def on_ready():
  print(f'{bot.user} has connected to Discord!')
    
@bot.command(aliases = ['who', 'saha']) #alias untuk command (pake prefix)
async def siapa(ctx): #nama command (harus dipanggil pakai prefix diatas)
  message = ctx.channel
  await message.send("kamu adalah {}".format(ctx.author.nick))

@bot.command()
async def ping(ctx):
  await ctx.channel.send(f'{round(bot.latency*1000)}ms')

bot.run("NzI3ODY2MDUxNTU5MTYxOTM2.XvyHYg.vxxKbFe1QnCniBhNMkODispYla0")