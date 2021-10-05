from discord import Embed
from discord_ui import Button
from hentai import Hentai, Sort, Format
from helpers.ui import UI
from random import randint
from requests.exceptions import HTTPError


class NHentaiHelpers():
    def generate_help_embed(self):
        embed = Embed(color=randint(0, 0xffffff), title='Hentai Help')
        embed.add_field(name='Description', value='Browse nhentai.net tanpa VPN')
        embed.add_field(name='Usage', value='`!h random`\n`!h search <search query>`\n`!h read <id doujin>`', inline=False)
        embed.add_field(name='Note', value='Kunjungi https://nhentai.net/info/ untuk mengetahui search query apa saja yang valid', inline=False)

        return embed

    def generate_list_hentai_embed(self, doujin, curr_index: int, max_index: int, disable_components: bool=False):
        components = [
            Button(custom_id='hentai_first', color='blurple', emoji=UI.first_arrow, disabled=curr_index==1 or disable_components),
            Button(custom_id='hentai_prev', color='blurple', emoji=UI.previous_arrow, disabled=curr_index==1 or disable_components),
            Button(custom_id='delete', color='red', label='Delete', disabled=False),
            Button(custom_id='hentai_next', color='blurple', emoji=UI.next_arrow, disabled=max_index==1 or (curr_index==max_index) or disable_components),
            Button(custom_id='hentai_last', color='blurple', emoji=UI.last_arrow, disabled=max_index==1 or (curr_index==max_index) or disable_components),
        ]
        
        tags = [tag.name for tag in doujin.tag]
        artists = [artist.name for artist in doujin.artist]
        languages = [language.name for language in doujin.language]
        

        embed = Embed(title=f'{doujin.title(Format.Pretty)}', color=randint(0, 0xffffff))
        embed.set_image(url=doujin.thumbnail)        
        embed.add_field(name='Code', value=doujin.id)
        embed.add_field(name='Artist', value=', '.join(artists))
        embed.add_field(name='Release Date', value=str(doujin.upload_date)[0:10])
        embed.add_field(name='Language', value=', '.join(languages))
        embed.add_field(name='Pages Number', value=doujin.num_pages)
        embed.add_field(name="Start Reading", value=doujin.url)
        embed.set_footer(text=f"Tags: {', '.join(tags)} | {curr_index}/{max_index}")
        
        return embed, components

    def generate_read_hentai_embed(self, title, page, curr_index: int, max_index: int, disable_components: bool=False):
        components = [
            Button(custom_id='hentai_first', color='blurple', emoji=UI.first_arrow, disabled=curr_index==1 or disable_components),
            Button(custom_id='hentai_prev', color='blurple', emoji=UI.previous_arrow, disabled=curr_index==1 or disable_components),
            Button(custom_id='delete', color='red', label='Delete', disabled=False),
            Button(custom_id='hentai_next', color='blurple', emoji=UI.next_arrow, disabled=max_index==1 or (curr_index==max_index) or disable_components),
            Button(custom_id='hentai_last', color='blurple', emoji=UI.last_arrow, disabled=max_index==1 or (curr_index==max_index) or disable_components),
        ]     

        embed = Embed(title=title, color=randint(0, 0xffffff))
        embed.set_image(url=page)        
        embed.set_footer(text=f'{curr_index}/{max_index}')
        
        return embed, components
