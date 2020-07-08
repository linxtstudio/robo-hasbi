import discord
from discord import Embed
from discord.ext import commands
from discord.ext.commands import ExtensionError
import random
import os
import robiconf
from robiconf.bot_configuration import Token, BotInstance

bot = BotInstance.bot #ngambil object bot dari robiconf

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

bot.load_extension('cogs.event')

@bot.event
async def on_ready():
  print(f'{bot.user} has connected to Discord!')

bot.run(Token.token)