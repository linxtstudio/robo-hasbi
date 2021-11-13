from discord import Embed, File
from discord_ui import Button
from helpers.ui import UI
from pixivpy3 import AppPixivAPI
import requests
import os

"""
Disclaimer: this weirdly structured architecture is not entirely my fault.
The asshole pixiv decided that the only one that can access their cdn api is the on that have japanese proxy.
And since discord embed only allowing image url to be embedded (not the actual file itself).
So, my workaround is to just download the file using japanese proxy -> upload the file to my MEDIA_SERVER service -> then using that api in the discord emmbed url

P.S pixiv doesn't have any right to be this big of a piece of shit
"""

class PixivWrapper:
    REFRESH_TOKEN = 'sn4a0zjnCWGibzq-9b6TvtmHHhorICSupH5fkGneDXU'
    ACCESS_TOKEN = ''
    USER_AGENT = 'PixivAndroidApp/5.0.234 (Android 11; Pixel 5)'
    AUTH_TOKEN_URL = 'https://oauth.secure.pixiv.net/auth/token'
    CLIENT_ID = 'MOBrBDS8blbauoSck0ZfDbtuzpyT'
    CLIENT_SECRET = 'lsACyCD94FhDUtGTXi3QzcFE2uU1hqtDaKeqrdwj'
    MEDIA_SERVER = 'https://image-server-app.harizmunawar.repl.co'
    PIXIV_STORAGE_PATH = f'{os.getcwd()}\storage\pixiv'
    client = AppPixivAPI()

    def __init__(self):
        if not os.path.isdir(self.PIXIV_STORAGE_PATH):
            os.makedirs(self.PIXIV_STORAGE_PATH)

        self.ACCESS_TOKEN = self.refresh(self.REFRESH_TOKEN)['access_token']
        self.client.set_auth(self.ACCESS_TOKEN, self.REFRESH_TOKEN)

    def refresh(self, refresh_token):
        response = requests.post(
            self.AUTH_TOKEN_URL,
            data={
                "client_id": self.CLIENT_ID,
                "client_secret": self.CLIENT_SECRET,
                "grant_type": "refresh_token",
                "include_policy": "true",
                "refresh_token": refresh_token,
            },
            headers={"User-Agent": self.USER_AGENT},
        )
        return response.json()

    def get_image_extension(self, image_url):
        return image_url[-3:]

    def check_image_exists(self, illust_id):
        list_image = [filename[:-3] for filename in os.listdir(self.PIXIV_STORAGE_PATH)]
        return str(illust_id) in list_image

    def save_image(self, illust):
        url = illust.image_urls.large
        filename = f'{str(illust.id)}.{self.get_image_extension(url)}'
        path_image = f'{self.PIXIV_STORAGE_PATH}/{filename}'
        
        # Checking if file with that name already exists in the media server (performance boost)
        resp = requests.get(f'{self.MEDIA_SERVER}/download/{str(illust.id)}.{self.get_image_extension(url)}')
        if resp.status_code == 200:
            return filename
        
        # Downloading the image then uploading it to the media server
        self.client.download(url, path=self.PIXIV_STORAGE_PATH, name=f'{str(illust.id)}.{self.get_image_extension(url)}')
        with open(path_image, 'rb') as img:
            name_img = os.path.basename(path_image)
            files = {'file': (name_img, img, 'multipart/form-data', {'Expires': '0'}) }
            with requests.Session() as s:
                r = s.post(f'{self.MEDIA_SERVER}/upload', files=files)
        
        os.unlink(path_image)
        return filename

    def generate_embed(self, post, max_index, curr_index, disable_components: bool=False):
        filename = self.save_image(post)
        tags = []
        for tag in post.tags:
            if not tag['translated_name'] and not any(map(tag['name'].__contains__, ['bookmark', 'user'])):
                tags.append(tag['name'])

            if tag['translated_name'] and not any(map(tag['translated_name'].__contains__, ['bookmark', 'user'])):
                tags.append(tag['translated_name'])

        components = [
            Button(custom_id='pixiv_first', color='grey', emoji=UI.first_arrow, disabled=curr_index==1 or disable_components),
            Button(custom_id='pixiv_prev', color='blurple', emoji=UI.previous_arrow, disabled=curr_index==1 or disable_components),
            Button(custom_id='delete', color='red', label='Delete', disabled=False),
            Button(custom_id='pixiv_next', color='blurple', emoji=UI.next_arrow, disabled=max_index==1 or (curr_index==max_index) or disable_components),
            Button(custom_id='pixiv_last', color='grey', emoji=UI.last_arrow, disabled=max_index==1 or (curr_index==max_index) or disable_components),
        ]

        embed = Embed(title=post.title[:255], color=0x0045ff)
        embed.set_author(name=f'By {post.user.name[:50]} (@{post.user.account[:50]}) on {post.create_date[:10]}', icon_url='https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/Pixiv_Icon.svg/450px-Pixiv_Icon.svg.png', url=f'https://www.pixiv.net/en/users/{post.user.id}')
        embed.add_field(name='Tags', value=', '.join(tags), inline=False)
        embed.set_image(url=f'{self.MEDIA_SERVER}/download/{filename}')
        embed.set_footer(text=f'👁‍🗨{post.total_view} ─── {curr_index} of {max_index} illustration ─── ID: {post.id}')

        return embed, components