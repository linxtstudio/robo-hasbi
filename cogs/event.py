from bot import debug
from discord.ext import commands
from discord import Activity, ActivityType, Embed, Member, CategoryChannel
from helpers import get_auto_voice_category, get_bot_dev_channel, get_ruang_pribadi_channel
from helpers.ready_message_helpers import ReadyMessage
from helpers.ui import UI

class Event(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.change_status.start()

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        error = error.original if hasattr(error, 'original') else error
        if hasattr(ctx.command, 'on_error'):
            return

        if debug:
            await ctx.send(embed=UI.error_embed(error))

        raise error

    @commands.Cog.listener()
    async def on_button_press(self, btn, **kwargs):
        if btn.custom_id == 'delete':
            await btn.message.delete()

    @commands.Cog.listener()
    async def on_ready(self):
        channel = get_bot_dev_channel(self.bot)
        
        await self.bot.change_presence(activity=Activity(type=ActivityType.watching, name="Pemandangan Jogja"))
        await channel.send(ReadyMessage('storage/ready_message.json').get_random())
        print(f'{self.bot.user} has connected to Discord!')

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        ruang_pribadi_channel = get_ruang_pribadi_channel(self.bot)
        auto_voice_category = get_auto_voice_category(self.bot)

        if after.channel == ruang_pribadi_channel:
            new_channel_name = f'Ruang Rapat {member.name}'
            new_channel = await member.guild.create_voice_channel(new_channel_name, category=auto_voice_category)
            await member.move_to(new_channel)

            await self.bot.wait_for('voice_state_update', check=lambda a, b, c: not bool(len(new_channel.members)))
            await new_channel.delete()

def setup(bot):
    bot.add_cog(Event(bot))