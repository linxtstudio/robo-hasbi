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

    def check_image_exists(self, illust):
        # Check whether the image already exists in the media server, then returning the filename if it is. e.g 9876123.jpg
        resp = requests.get(f'{self.MEDIA_SERVER}/download/{str(illust.id)}.{self.get_image_extension(illust.image_urls.large)}')
        
        return f'{str(illust.id)}.{self.get_image_extension(illust.image_urls.large)}' if resp.status_code == 200 else None

    def download_image(self, illust):
        self.client.download(illust.image_urls.large, path=self.PIXIV_STORAGE_PATH, name=f'{str(illust.id)}.{self.get_image_extension(illust.image_urls.large)}')

    def upload_image(self, image_path):
        with open(image_path, 'rb') as img:
            name_img = os.path.basename(image_path)
            files = {'file': (name_img, img, 'multipart/form-data', {'Expires': '0'}) }
            with requests.Session() as s:
                s.post(f'{self.MEDIA_SERVER}/upload?folder=robi-pixiv', files=files)

    def save_image(self, illust):
        url = illust.image_urls.large
        filename = f'{str(illust.id)}.{self.get_image_extension(url)}'
        image_path = f'{self.PIXIV_STORAGE_PATH}/{filename}'
        
        if not self.check_image_exists(illust):
            self.download_image(illust)
            self.upload_image(image_path)
            os.unlink(image_path)

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
        embed.set_image(url=f'{self.MEDIA_SERVER}/download/{filename}?folder=robi-pixiv')
        embed.set_footer(text=f'👁‍🗨{post.total_view} ─── {curr_index} of {max_index} illustration ─── ID: {post.id}')

        return embed, components