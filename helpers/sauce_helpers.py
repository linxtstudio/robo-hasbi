from base64 import b64decode

from discord.embeds import Embed
from discord_ui import Button
from helpers.ui import UI
from random import randint
from saucenao_api import AIOSauceNao

class SauceWrapper():
    key = b64decode('ZTZlNjFhY2RhYzE4Y2Q4ZWZhOWZhZWQ2MDY3MWY1Njc2NDY2NjE4Zg==')
    client = AIOSauceNao(key.decode('utf-8'))

    async def get_sauce(self, url: str):
        async with self.client as aio:
            results = await aio.from_url(url)

        return results or None

    def generate_embed(self, sauce, max_index: int, curr_index: int, disable_components: bool=False):
        components = [
            Button(custom_id='sauce_first', color='blurple', emoji=UI.first_arrow, disabled=curr_index==1 or disable_components),
            Button(custom_id='sauce_prev', color='blurple', emoji=UI.previous_arrow, disabled=curr_index==1 or disable_components),
            Button(custom_id='delete', color='red', label='Delete', disabled=False),
            Button(custom_id='sauce_next', color='blurple', emoji=UI.next_arrow, disabled=max_index==1 or (curr_index==max_index) or disable_components),
            Button(custom_id='sauce_last', color='blurple', emoji=UI.last_arrow, disabled=max_index==1 or (curr_index==max_index) or disable_components),
        ]

        embed = Embed(color=randint(0, 0xffffff), title='Hasbi Image Search')
        embed.add_field(name='Author', value=sauce.author, inline=True)
        embed.add_field(name='Title', value=sauce.title, inline=True)
        embed.add_field(name='HD URL', value=sauce.urls[0], inline=False)
        embed.set_image(url=sauce.thumbnail)
        embed.set_footer(text=f'Similarity: {sauce.similarity}%')

        return embed, components
