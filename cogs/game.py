import discord
from random import choice
from discord.ext import commands
import string

class Game(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hangman(self, ctx):
        def check(m):
            return m.author == ctx.author

        random_words = choice(hangman_words())
        words = random_words['word']
        deskripsi = random_words['deskripsi']
        word_succes, lose = [], 0
        choose_word = []
        words_answer = ''
        alphabet = ''
        alphabet_list = list(string.ascii_uppercase)

        for alpha in alphabet_list:
            alphabet += ''.join(alpha+' ')

        for word in words:
            if word != ' ':
                words_answer += ' '.join(' -')
            else:
                words_answer += ' '.join('  ')

        embed = discord.Embed(title=words_answer, color=0x00ff00, description='chance : '+str(3-lose)+'\ndescription: '+deskripsi)
        embed.set_footer(text = alphabet)
        embed.set_image(url="https://selftaught.blog/wp-content/uploads/2017/12/hangman-287x300.jpg")
        await ctx.channel.send(embed = embed)

        while len(word_succes) < len(dict.fromkeys(words.lower().replace(" ", ""))):
            words_answer = ''
            alphabet = ''
            answer = await self.bot.wait_for("message", check=check, timeout=60)

            if answer.content.lower() == 'stop': break
            if(answer.content[0] != '!'):
                if len(answer.content) > 1:
                    await ctx.channel.send('Tolong masukan huruf seperti `a` atau `b` saja')
                else:
                    if answer.content.lower() not in choose_word:
                        if answer.content.lower() in [word.lower() for word in words]:
                            word_succes.append(answer.content.lower())
                        else: 
                            lose += 1
                        choose_word.append(answer.content.lower())

                        for word in words.lower():
                            if word in word_succes: 
                                words_answer += ' '.join(' '+word.upper())
                            else: 
                                if word != ' ':
                                    words_answer += ' '.join(' -')
                                else:
                                    words_answer += ' '.join('  ')
                        
                        for alpha in alphabet_list:
                            if alpha.lower() not in choose_word:
                                alphabet += ''.join(alpha+' ')

                        embed = discord.Embed(title=words_answer, color=0x00ff00, description='chance : '+str(3-lose)+'\ndescription: '+deskripsi)
                        embed.set_footer(text = alphabet)
                        embed.set_image(url="https://selftaught.blog/wp-content/uploads/2017/12/hangman-287x300.jpg")
                        await ctx.channel.send(embed = embed)

                        if lose >= 3: 
                            await ctx.channel.send('Selamat Kamu kalah')
                            break
                    else:
                        await ctx.channel.send('Huruf ini sudah terpakai')
        else:
            await ctx.channel.send('Selamat kamu menang')

def hangman_words():
    return  [
                {'word': 'Mamet', 'deskripsi': 'Kepsek SMKN 1 Cimahi'},
                {'word': 'Game', 'deskripsi': 'Sebuah Permainan'},
                {'word': 'Python', 'deskripsi': 'Salah satu bahasa pemrograman yang diminati'},
                {'word': 'Java', 'deskripsi': 'Bahasa pemrograman yang menyiksa'},
                {'word': 'Dildo', 'deskripsi': 'Kesukaan Adrian'},
                {'word': 'Angkot Mania', 'deskripsi': 'Digibit Project'},
                {'word': 'Man Behind The Gun', 'deskripsi': 'Guru Bahasa Indonesia'},
            ]


def setup(bot):
    bot.add_cog(Game(bot))