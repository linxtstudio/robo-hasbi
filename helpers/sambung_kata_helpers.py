from discord import Embed
from discord_ui import Button
from helpers.exceptions import NotEnoughPlayerException, ZeroRollException
from helpers.kbbi import AutentikasiKBBI, KBBI, TidakDitemukan
from os import path
from operator import itemgetter
from random import randint
import json
import re

class SambungKataPlayer:
    def __init__(self):
        self.players = []
        self.ready = []
        self.active_player = []
        self.hasbi_playing = False
        self.active_index = 0
    
    def already_joined(self, player):
        return any(_player['id'] == player.id for _player in self.players)

    def add_player(self, player, is_hasbi: bool=False):
        if not self.already_joined(player):
            self.players.append({'player': player, 'id': player.id, 'roll': 3, 'point': 0})

        if is_hasbi:
            self.hasbi_playing = is_hasbi

    def remove_player(self, player):
        if self.already_joined(player):
            self.players.remove(self.get_player(player))

    def get_active_player(self):
        return self.players[self.active_index % len(self.players)]

    def next_player(self):
        self.active_index += 1
        return self.get_active_player()

    def start(self, player):
        if player in self.ready and len(self.players) < 2: raise NotEnoughPlayerException
        if self.already_joined(player): self.ready.append(self.get_player(player))

    def get_player(self, player):
        return [_player for _player in self.players if _player['id'] == player.id][0]

    def get_roll(self, player):
        return [_player['roll'] for _player in self.players if _player['id'] == player.id][0]

    def get_point(self, player):
        return [_player['point'] for _player in self.players if _player['id'] == player.id][0]

    def add_point(self, player, point):
        _player = self.get_player(player)
        _player['point'] += point

    def deduct_roll(self, player):
        _player = self.get_player(player)
        _player['roll'] -= 1 if _player['roll'] > 0 else 0

class SambungKataHelper(SambungKataPlayer):
    def __init__(self, cookie_path: str='storage/kuki_kbbi.json', word_list_path: str='storage/kata-dasar-indonesia.txt'):
        super().__init__()
        self.cookie_path = cookie_path
        self.word_list_path = word_list_path
        self.words = []
        self.current_word = ''
        self.started = False
        self.auth_kbbi = self.login_kbbi()

    def fetch_all_words(self):
        with open(self.word_list_path, 'r') as file:
            for line in file:
                line = line.strip('\n')
                pos = re.findall(r'\(.*?\)', line)
                self.words.append(line.replace(str(pos[0]), '').rstrip().lower())

        return self.words

    def get_random_words(self):
        if not len(self.words):
            self.fetch_all_words()

        return self.words[randint(0, len(self.words)-1)]

    def get_word_from_kbbi(self, word: str):
        try:
            if not self.auth_kbbi: self.login_kbbi()
            kata = KBBI(word, self.auth_kbbi)
            return kata.serialisasi()
        except TidakDitemukan:
            return False

    def login_kbbi(self):
        try:
            if path.exists(self.cookie_path):
                auth = AutentikasiKBBI(lokasi_kuki=self.cookie_path)
                auth.ambil_kuki()
            else:
                auth = AutentikasiKBBI('valdain.shadow@gmail.com', 'iamrobohasbi', lokasi_kuki=self.cookie_path)
                auth.simpan_kuki()
            return auth
        except:
            return None

    def check_start_game(self):
        self.started =  len(self.players) > 1 and ((self.hasbi_playing and len(self.players)-1 == len(self.ready)) or (len(self.players) == len(self.ready)))

        return self.started

    def roll(self, player):
        for data in self.player_data:
            if data['id'] == player.id:
                if data['roll'] > 0:
                    data['roll'] -= 1
                else:
                    raise ZeroRollException

        return self.get_random_words()

    def get_last_syllable(self, word):
        kata = word['entri'][0]['nama']

        return kata.split('.')[-1]

    def answer(self, word):
        self.add_point(self.get_active_player()['player'], len(word))
        self.next_player()

        return word

    def generate_not_enough_player_embed(self):
        embed = Embed(title='Tidak Bisa Memulai Permainan', color=0xff0000)
        embed.add_field(name='\u200b', value='Butuh setidaknya dua pemain untuk memulai permainan')

        return embed

    def generate_lobby_embed(self, players: list):
        string_players = ''
        for player in players:
            string_players += f'<:reply:885797725327745085>{player["player"].mention}\n'

        components = [
            Button(custom_id='sk_start', label='Start', color='green'),
            Button(custom_id='sk_join', label='Join', color='blurple'),
            Button(custom_id='sk_hasbi', label='Ajak Hasbi', color='blurple'),
            Button(custom_id='sk_exit', label='Exit', color='red')
        ]

        embed = Embed(title='Hasbi Sambung Kata', color=randint(0, 0xffffff))
        embed.add_field(name='Players:', value=string_players or 'Belum Ada Pemain')
        embed.set_footer(text=f'{len(self.ready)}/{len(self.players)-1 if self.hasbi_playing else len(self.players)} Pemain Sudah Menekan Tombol Start' if len(self.players) >= 2 else '')

        return embed, components
    
    def generate_round_embed(self, word):
        makna_string = ''
        player_string = ''

        for entri in word['entri']:
            for makna in entri['makna'][0:3]:
                makna_string += '<:reply:885797725327745085>'
                for kelas in makna['kelas']:
                    makna_string += f'({str(kelas["kode"])}) '
                makna_string += f'{" ".join(makna["submakna"])}\n'

        for player in self.players:
            player_string += '<:reply:885797725327745085>'
            if player == self.get_active_player():
                player_string += '<:next_arrow:885775938871263302> '
            player_string += f'{player["player"].mention} | Roll: {self.get_roll(player["player"])} | Point: {self.get_point(player["player"])}\n'

        embed = Embed(title='Hasbi Sambung Kata', color=randint(0, 0xffffff))
        embed.add_field(name=str(word['entri'][0]['nama']).upper(), value=makna_string)
        embed.add_field(name='Player', value=player_string, inline=False)

        return embed

    def hasbi_ai(self, question):
        data = []
        last_syllable = self.get_last_syllable(question)
        possible_answer = [word for word in self.words if word.startswith(last_syllable)]

        if not possible_answer: return 'roll'

        for answer in possible_answer:
            kbbi_word = self.get_word_from_kbbi(answer)
            last_syllable = self.get_last_syllable(kbbi_word)
            data.append(
                {
                    'word': answer,
                    'point': len(answer),
                    'possible_next': len([word for word in self.words if word.startswith(last_syllable)])
                }
            )

        sorted_data = sorted(data, key=itemgetter('possible_next'))
        same_possible_next = [data for data in sorted_data if data['possible_next'] == sorted_data[0]['possible_next']]

        if len(same_possible_next) > 1:
            sorted_data = sorted(sorted_data, key=itemgetter('point'), reverse=True)

        for data in sorted_data:
            if self.get_word_from_kbbi(data['word']): return self.answer(data['word'])
