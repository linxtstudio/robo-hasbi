from bot import debug
from discord.ext import commands
from discord import Activity, ActivityType, Embed, Member, CategoryChannel
from helpers import get_auto_voice_category, get_bot_dev_channel, get_ruang_pribadi_channel
from helpers.ready_message_helper import ReadyMessage
from helpers.ui import UI

class Event(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        error = error.original if hasattr(error, 'original') else error
        if hasattr(ctx.command, 'on_error'):
            return

        if debug:
            await ctx.send(embed=UI.error_embed(error))

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
        
        await self.bot.change_presence(activity=Activity(type=ActivityType.watching, name="Pemandangan Jogja"))
        await channel.send(ReadyMessage('storage/ready_message.json').get_random())
        print(f'{self.bot.user} has connected to Discord!')

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        bot_dev_channel = get_bot_dev_channel(self.bot)
        ruang_pribadi_channel = get_ruang_pribadi_channel(self.bot)
        auto_voice_category = get_auto_voice_category(self.bot)

        if after.channel == ruang_pribadi_channel:
            new_channel_name = f'Ruang Rapat {member.name}'
            new_channel = await member.guild.create_voice_channel(new_channel_name, category=auto_voice_category)
            await member.move_to(new_channel)

            def check(a,b,c):
                return len(new_channel.members) == 0
            await self.bot.wait_for('voice_state_update', check=check)
            await new_channel.delete()

def setup(bot):
    bot.add_cog(Event(bot))