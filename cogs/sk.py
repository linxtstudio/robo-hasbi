from discord.ext import commands
from helpers.exceptions import NotEnoughPlayerException, ZeroRollException
from helpers.sambung_kata_helpers import SambungKataHelper
from helpers.kbbi import TidakDitemukan
from random import shuffle

class SambungKata(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['sk'])
    async def sambungkata(self, ctx):
        game = SambungKataHelper()

        embed, components = game.generate_lobby_embed(players=game.players)
        lobby = await ctx.send(embed=embed, components=components)

        try:
            while True:
                btn = await lobby.wait_for('button', self.bot, timeout=300)
                await btn.respond(ninja_mode=True)
                
                if btn.custom_id == 'sk_start':
                    try:
                        game.start(btn.author)
                    except NotEnoughPlayerException:
                        await ctx.send(embed=game.generate_not_enough_player_embed())
                if btn.custom_id == 'sk_join': game.add_player(btn.author)
                if btn.custom_id == 'sk_hasbi': game.add_player(btn.message.author, is_hasbi=True)
                if btn.custom_id == 'sk_exit': game.remove_player(btn.author)

                embed, components = game.generate_lobby_embed(players=game.players)
                await lobby.edit(embed=embed, components=components)
                if game.check_start_game(): raise TimeoutError
        except TimeoutError:
            await lobby.delete()
            if not game.started: return await ctx.send(embed=game.generate_not_enough_player_embed())

        # Start The Game
        shuffle(game.players)
        word = game.get_word_from_kbbi(game.get_random_words())
        game.current_word = word
        embed = game.generate_round_embed(word=word)
        round = await ctx.send(embed=embed)

        def check_answer(m):
            if not game.get_word_from_kbbi(m.content.lower): return False

            correct_player = m.author == game.get_active_player()['player']
            correct_answer = m.content.lower().startswith(game.get_last_syllable(game.current_word)) and m.content.lower() in game.words
            
            return correct_player and correct_answer


        try:
            while True:
                if game.get_active_player()['player'].bot:
                    async with ctx.typing():
                        hasbi_answer = game.hasbi_ai(word)
                        await ctx.send(hasbi_answer)
                        word = game.get_word_from_kbbi(hasbi_answer)
                else:
                    answer = await self.bot.wait_for('message', check=check_answer, timeout=20)
                    reply = answer.content.lower()

                    if reply == 'roll':
                        try: game.roll(game.get_active_player()['player'])
                        except ZeroRollException: pass
                    
                    word = game.get_word_from_kbbi(game.answer(reply))

                game.current_word = word
                embed = game.generate_round_embed(word=word)
                await round.delete()
                round = await ctx.send(embed=embed)
        except TimeoutError:
            await ctx.send('kelamaan mikir')

def setup(bot):
    bot.add_cog(SambungKata(bot))