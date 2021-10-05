from bot import debug
from discord.ext import commands
from discord import Activity, ActivityType, Embed, Member
from discord_ui import Listener
from helpers import get_bot_dev_channel
from helpers.ready_message_helper import ReadyMessage

class Event(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        error = error.original if hasattr(error, 'original') else error
        if hasattr(ctx.command, 'on_error'):
            return

        if debug:
            await ctx.send(embed=Embed(title=error, color=0xff0000))

        raise error

    @commands.Cog.listener('on_reaction_add')
    async def on_reaction_add(self, reaction, user: Member):
        pass

    @commands.Cog.listener('on_button_press')
    async def on_button(self, btn, **kwargs):
        if btn.custom_id == 'delete':
            await btn.message.delete()

    @commands.Cog.listener()
    async def on_ready(self):
        channel = get_bot_dev_channel(self.bot)
        
        await self.bot.change_presence(activity=Activity(type=ActivityType.listening, name="Walikelas"))
        await channel.send(ReadyMessage('storage/ready_message.json').get_random())
        print(f'{self.bot.user} has connected to Discord!')


def setup(bot):
    bot.add_cog(Event(bot))