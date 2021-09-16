from discord.ext import commands
from discord_ui import UI

class BotInstance:
    bot = commands.Bot('!')
    ui = UI(client=bot)