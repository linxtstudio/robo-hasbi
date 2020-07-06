import discord
from discord import Embed
from discord.ext import commands
from discord.ext.commands.errors import *
import random
import os
import robiconf
from robiconf.bot_configuration import Token, BotInstance

bot = BotInstance.bot #ngambil object bot dari robiconf

@bot.command(aliases=['re'])
async def refresh(ctx, extension):
  bot.unload_extension(f'cogs.{extension}')
  bot.load_extension(f'cogs.{extension}')
  await ctx.channel.send(f'Cogs {extension} Berhasil di Refresh')

@refresh.error
async def load_error(ctx, error):
  if isinstance(error, commands.CommandInvokeError):
      bot.load_extension(f'cogs.{extension}')
      await ctx.channel.send(f'Cogs {extension} Berhasil di Refresh')
  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.channel.send('Kesalahan Penggunan Command.\n > !load <namacogs>')
  raise error

for filename in os.listdir('./cogs'):
  if filename.endswith('.py'):
    bot.load_extension(f'cogs.{filename[:-3]}')

@bot.event
async def on_ready():
  print(f'{bot.user} has connected to Discord!')

bot.run(Token.token)