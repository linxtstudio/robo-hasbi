from discord import Embed
from discord_ui import Button
from random import randint

class AkinatorWrapper():
    def generate_embed(self, question: str="", guess=None, guessing: bool=False, disable_components: bool=False):
        embed = Embed(color=randint(0, 0xffffff), title='Hasbi Menebak Karakter')

        if guessing:
            embed.add_field(name=guess['name'], value=guess['description'])
            embed.set_thumbnail(url=guess['absolute_picture_path'])

            components = [
                Button(custom_id='aki_benar', label='Benar', color='green', disabled=disable_components),
                Button(custom_id='aki_salah', label='Salah', color='red', disabled=disable_components)
            ]
        else:
            embed.description = question.title()

            components = [
                Button(custom_id='aki_yes', label='Ya', color='green', disabled=disable_components),
                Button(custom_id='aki_maybe', label='Mungkin', color='blurple', disabled=disable_components),
                Button(custom_id='aki_idk', label='Gatau', color='blurple', disabled=disable_components),
                Button(custom_id='aki_no', label='Tidak', color='red', disabled=disable_components),
                Button(custom_id='aki_stop', label='Stop', color='red', disabled=disable_components),
            ]

        return embed, components

    def generate_error_embed(self, message: str=''):
        embed = Embed(color=0xd62929, title='Hasbi Menebak Karakter')
        embed.add_field(name='❌  Permainan Dihentikan', value=message)

        return embed
