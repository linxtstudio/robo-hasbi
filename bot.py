from base64 import b64decode
from random import randint
from discord import Embed, Activity, ActivityType
from discord_ui import UI
from discord.ext import commands
from helpers import loadall, unloadall
from itertools import cycle
from os import listdir
from threading import Thread
from webhooks import loker
import ping

hasbi = commands.Bot('!')
ui = UI(client=hasbi)
token_utf8 = b64decode('TnpJM09EWTJNRFV4TlRVNU1UWXhPVE0yLlh3Tk5BUS5ZSk8wWHlfMHV4MzEyMG5GMURYRml1SVQyLW8=')
debug = True
status = cycle(['Pemandangan Jogja','Dokumenter Kehidupan Adolf Hitler'])

class CustomHelp(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        e = Embed(title="Hasbi", color=randint(0, 0xffffff), description='')
        for page in self.paginator.pages:
            e.description += page
        await destination.send(embed=e)

if __name__ == '__main__':
    for filename in listdir('./cogs'):  
        if filename.endswith('.py'):
            try: hasbi.load_extension(f'cogs.{filename[:-3]}')
            except: pass

    # A handy tools that gonna help us later
    hasbi.help_command = CustomHelp()
    hasbi.add_command(loadall)
    hasbi.add_command(unloadall)

    # Start Threading
    Thread(target=ping.exposed_api).start()
    Thread(target=loker.cari_loker).start()

    hasbi.run(token_utf8.decode('utf-8'), bot=True, reconnect=True)
