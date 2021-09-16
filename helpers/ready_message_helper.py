from discord_ui import Button
from discord.ext.commands.errors import CommandInvokeError
from helpers.ui import UI
from discord import Embed
from helpers import get_max_page
import json
import random

class ReadyMessage:
    def __init__(self, storage_path: str):
        self.storage_path = storage_path

    def get_all(self, as_list: bool=False):
        with open (self.storage_path) as file:
            data = json.load(file)
        
        if as_list:
            data = [message['message'] for message in data['messages']]
            
        return data

    def dump_all(self, data):
        with open('storage/ready_message.json', 'w') as file:
            json.dump(data, file, indent=4)

    def get_random(self):
        data = self.get_all(as_list=True)

        return random.choice(data)

    def refresh_id(self):
        data = self.get_all()

        for index, message in enumerate(data['messages']):
            message['id'] = index + 1

        return self.dump_all(data)

    def add(self, message: str):
        data = self.get_all()

        message = {
            'id': len(self.get_all(as_list=True)) + 1,
            'message': message
            }
        data['messages'].append(message)
    
        self.dump_all(data)

        return self.get_all()

    def remove(self, id: int):
        data = self.get_all()
        new_list = []

        for message in data['messages']:
            if message['id'] == id:
                continue

            new_list.append(message)

        if data['messages'] == new_list:
            raise CommandInvokeError('Pesan dengan ID tersebut tidak ditemukan')

        data['messages'] = new_list

        self.dump_all(data)
        self.refresh_id()

        return self.get_all()

    def generate_embed(self, page=1, disable_components=False):
        data = self.get_all()['messages']
        max_page = get_max_page(len(data), 5)
        last_index = page * 5
        first_index = last_index - 5

        components = [
            Button(custom_id='rm_prev', color='blurple', emoji=UI.previous_arrow, disabled=page==1 or disable_components),
            Button(custom_id='rm_next', color='blurple', emoji=UI.next_arrow, disabled=page==max_page or disable_components),
        ]

        embed = Embed(title='List Ready Message', color=random.randint(0, 0xffffff))
        for message in data[first_index:last_index]:
            embed.add_field(name=f'ID: {message["id"]}', value=f'<:reply:885797725327745085>{message["message"]}', inline=False)
        embed.set_footer(text=f'Page {page}/{max_page}')

        return embed, components
