from asyncio import TimeoutError
from discord import Embed
from discord.ext import commands
from helpers.ready_message_helpers import ReadyMessage
from random import randint

from helpers.ui import UI


class Settings(commands.Cog):
    rm = ReadyMessage('storage/ready_message.json')

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def load(self, ctx, extension):
        self.bot.load_extension(f'cogs.{extension}')
        await ctx.message.add_reaction('👍')

    @commands.command()
    async def unload(self, ctx, extension):
        if extension == 'setting':
            return await ctx.send(embed=UI.error_embed("Dilarang unload setting 😠"))

        self.bot.unload_extension(f'cogs.{extension}')
        await ctx.message.add_reaction('👍')

    @commands.command(aliases=['re'])
    async def reload(self, ctx, extension):
        self.bot.reload_extension(f'cogs.{extension}')
        await ctx.message.add_reaction('👍')

    @load.error
    @unload.error
    @reload.error
    async def loader_error(self, ctx, error):
        await ctx.message.add_reaction('👎')
        error_embed=Embed(color=0xd62929)
        error_embed.set_author(name=f"❌  {error.original}")
        await ctx.send(embed=error_embed)

    @commands.group(aliases=['rm'])
    async def readymessage(self, ctx):
        if ctx.invoked_subcommand is None:
            embed = Embed(title='Ready Message Help', color=randint(0, 0xffffff))
            embed.add_field(name='Description', value='Tambahin kata untuk diucapkan sama hasbi ketika dia restart')
            embed.add_field(name='Usage', value='`!rm add <kata yang mau ditambahkan>`\n`!rm list`\n`!rm remove <id dari kata yang mau dihapus>`', inline=False)

            await ctx.send(embed=embed)

    @readymessage.command()
    async def add(self, ctx, *, message: str):
        async with ctx.typing():
            self.rm.add(message.title())
            return await ctx.send(embed=UI.success_embed("Pesan sudah berhasil ditambahkan"))
    
    @readymessage.command()
    async def remove(self, ctx, id: int):
        async with ctx.typing():
            self.rm.remove(id)
            return await ctx.send(embed=UI.success_embed("Pesan sudah berhasil dihapus"))

    @readymessage.command(aliases=['list'])
    async def show(self, ctx):
        async with ctx.typing():
            page = 1
            embed, components = self.rm.generate_embed(page)
            rm = await ctx.send(embed=embed, components=components)

        try:
            while True:
                btn = await rm.wait_for('button', self.bot, timeout=60)
                await btn.respond(ninja_mode=True)

                if btn.custom_id == 'rm_next': page += 1
                if btn.custom_id == 'rm_prev': page -= 1

                embed, components = self.rm.generate_embed(page)
                await rm.edit(embed=embed, components=components)
        except TimeoutError:
            _, components = self.rm.generate_embed(page, disable_components=True)
            await rm.edit(components=components)


def setup(bot):
    bot.add_cog(Settings(bot))
