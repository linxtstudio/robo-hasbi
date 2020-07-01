import discord

client = discord.Client()

@client.event
async def on_ready():
  print(f'{client.user} has connected to Discord!')
    
@client.event
async def on_message(message): 
    if message.content.find("!sevi") != -1:
        await message.channel.send('halo om aku bot sevi')
    elif message.content.find("!tugas") != -1:
        await message.channel.send('libur tolollll')
client.run("NzI3ODY2MDUxNTU5MTYxOTM2.XvyHYg.vxxKbFe1QnCniBhNMkODispYla0")