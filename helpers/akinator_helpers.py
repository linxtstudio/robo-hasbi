from typing import Union
from discord import Embed
from discord_ui import Button
from random import randint

class AkinatorWrapper():
    def generate_embed(self, question: str="", guess=None, guessing: bool=False, disable_components: bool=False):
        if guessing:
            components = [
                Button(custom_id='aki_benar', label='Benar', color='green', disabled=disable_components),
                Button(custom_id='aki_salah', label='Salah', color='red', disabled=disable_components)
            ]
        else:
            components = [
                Button(custom_id='aki_yes', label='Ya', color='green', disabled=disable_components),
                Button(custom_id='aki_maybe', label='Mungkin', color='blurple', disabled=disable_components),
                Button(custom_id='aki_idk', label='Gatau', color='blurple', disabled=disable_components),
                Button(custom_id='aki_no', label='Tidak', color='red', disabled=disable_components),
                Button(custom_id='aki_stop', label='Stop', color='red', disabled=disable_components),
            ]

        embed = Embed(color=randint(0, 0xffffff), title='Hasbi Menebak Karakter')
        if guessing:
            embed.add_field(name=guess['name'], value=guess['description'])
            embed.set_image(url=guess['absolute_picture_path'])
        else:
            embed.add_field(name='\u200b', value=question.title())

        return embed, components

    def generate_timedout_embed(self, stopped_early: bool=False):
        message = 'Kamu menekan tombol stop' if stopped_early else 'Hasbi terlalu lelah menunggu jawaban kamu'
        embed = Embed(color=0xff0000, title='Hasbi Menebak Karakter')
        embed.add_field(name='Permainan Dihentikan', value=message)

        return embed

    def generate_final_embed(self, win :bool=True, message: str=''):
        embed = Embed(color=0x00ff00, title='Hasbi Menebak Karakter')
        if win:
            embed.add_field(name='\u200b', value='Tentu saja Hasbi tidak pernah salah')
        else:
            embed.add_field(name='Hasbi Menyerah', value=message)

        return embed
