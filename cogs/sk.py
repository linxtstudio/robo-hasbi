import asyncio
from discord_ui import Button
import random
from discord.ext import commands
from discord import Embed
from kbbi import KBBI, AutentikasiKBBI

class SK(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    def round_embed(self, kata: dict):
        embed = Embed(title='TESTING\t+7', color=random.randint(0, 0xFFFFFF))
        embed.add_field(name='\u200b', value="tes  /tès/\n1. (n)  ujian tertulis, lisan, atau wawancara untuk mengetahui pengetahuan, kemampuan, bakat, dan kepribadian seseorang\n2. (n)  percobaan untuk menguji kelaikan jalan suatu kendaraan bermotor umum; uji: berdasarkan -- yang dilakukan di balai pengujian kendaraan bermotor kendaraan jenis itu cukup baik untuk angkutan penumpang dan barang", inline=False)
        embed.add_field(name='Giliran', value='@moona')
        embed.add_field(name='Leaderboard', value='Player\tSkor\nNamaPlayer\tSkorPlayer')
        embed.set_footer(text='Lanjutkan kata dengan awalan "ting"')
        return embed

    def lobby_embed(self, player_list):
        embed = Embed(title='Sambung Kata', color=random.randint(0, 0xFFFFFF))
        embed.add_field(name='Player List', value='@moona\n@ngek')
        embed.set_footer(text='Timeout 5 Menit')

        return embed

    @commands.command(aliases=['sk'])
    async def sambungkata(self, ctx):
        players = []
        lobby = await ctx.channel.send(
            embed=self.lobby_embed(['okok']),
            components=[
                Button(custom_id='join_sk', label='Join', color='blurple', new_line=False),
                Button(custom_id='start_sk', label='Start', color='green', new_line=False),
                Button(custom_id='leave_sk', label='Leave', color='red', new_line=False),
            ]
        )

        while True:
            try:
                lobby_btn = await lobby.wait_for(self.bot, 'button', timeout=300)
                if lobby_btn.custom_id == 'join_sk':
                    pass
                
            except asyncio.TimeoutError:
                pass

        # await ctx.channel.send(
        #     embed=self.round_embed({'ok': 'ok'}),
        #     components=[
        #         Button(custom_id='join_sk', label='Join', color='green', new_line=False),
        #         Button(custom_id='roll', label='Roll', color='blurple', new_line=False),
        #     ]
        #     )


def setup(bot):
    bot.add_cog(SK(bot))