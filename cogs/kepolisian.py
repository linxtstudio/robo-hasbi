import discord
from discord.ext import commands
from configuration import BotInstance
from discord.ext.commands.errors import CheckFailure

bot = BotInstance.bot

class Kepolisian(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def lapor(self, ctx, tersangka: discord.Member, *alasan):
        polisi = discord.utils.get(ctx.message.guild.roles, name="Kepolisian")
        presiden = discord.utils.get(ctx.message.guild.roles, name="Presiden")
        tahanan = discord.utils.get(ctx.message.guild.roles, name="Tahanan")

        if not presiden in tersangka.roles or not polisi in tersangka.roles:
            laporan = ""
            for alasan in alasan:
                laporan = laporan + alasan + " "
            await ctx.channel.send(f'{ctx.author.mention} Melaporkan {tersangka.mention} Dengan Alasan "{laporan}"')
            need_react = await ctx.channel.send(f'{polisi.mention} Silahkan tambah react untuk memenjarakan tersangka')
            await need_react.add_reaction('👮')        

            penjara = await bot.wait_for('reaction_add', check=lambda reaction, user: (reaction.emoji == '👮' and user.name != 'Robo-Hasbi' and (polisi in user.roles or presiden in user.roles)))
            if penjara:
                await tersangka.add_roles(tahanan)
                await ctx.channel.send(f'> {ctx.author.mention} Melaporkan {tersangka.mention} Dengan Alasan "{laporan}"\nTersangka sudah diamankan dan dibawa ke penjara')
        else:
            await ctx.channel.send('Polisi dan Presiden tidak mungkin masuk penjara bodokkk!')

    @commands.command()
    @commands.has_any_role("Presiden", "Kepolisian")
    async def giverole(self, ctx, member: discord.Member, *, role: discord.Role):
        await member.add_roles(role)
        await ctx.channel.send(f"Role '{role}' telah diberikan kepada {member.mention}.")

    @commands.command()
    @commands.has_any_role("Presiden", "Kepolisian")
    async def removerole(self, ctx, member: discord.Member, *, role: discord.Role):
        await member.remove_roles(role)
        await ctx.channel.send(f"Role '{role}' telah dihapus dari {member.mention}.")

    @commands.command()
    @commands.has_any_role("Presiden", "Kepolisian")
    async def penjara(self, ctx, tersangka: discord.Member):
        polisi = discord.utils.get(ctx.message.guild.roles, name="Kepolisian")
        presiden = discord.utils.get(ctx.message.guild.roles, name="Presiden")
        tahanan = discord.utils.get(ctx.message.guild.roles, name="Tahanan")

        if not presiden in tersangka.roles or not polisi in tersangka.roles:
            await tersangka.add_roles(tahanan)
            await ctx.channel.send(f'{tersangka.mention} telah dimasukkan kedalam penjara, silahkan mulai interogasi')
        else:
            await ctx.channel.send('Polisi dan Presiden tidak mungkin masuk penjara bodokkk!')


def setup(bot):
    bot.add_cog(Kepolisian(bot))