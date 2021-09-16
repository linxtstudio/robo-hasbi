from base64 import b64decode
from discord_ui import UI
from discord.ext import commands
from helpers import ping, loadall, unloadall
from os import listdir
from threading import Thread
from webhooks import loker

hasbi = commands.Bot('!')
ui = UI(client=hasbi)
token_utf8 = b64decode('TnpJM09EWTJNRFV4TlRVNU1UWXhPVE0yLlh3Tk5BUS5ZSk8wWHlfMHV4MzEyMG5GMURYRml1SVQyLW8=')
debug = True

if __name__ == '__main__':
    if not debug:
        for filename in listdir('./cogs'):  
            if filename.endswith('.py'):
                try: hasbi.load_extension(f'cogs.{filename[:-3]}')
                except: pass

    hasbi.load_extension('cogs.sauce')
    hasbi.load_extension('cogs.setting')

    # A handy tools that gonna help us later
    hasbi.add_command(loadall)
    hasbi.add_command(unloadall)

    # Start Threading
    Thread(target=ping.exposed_api).start()
    Thread(target=loker.cari_loker).start()

    hasbi.run(token_utf8.decode('utf-8'), bot=True, reconnect=True)
