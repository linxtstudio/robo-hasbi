from akinator.async_aki import Akinator
from akinator.exceptions import AkiNoQuestions
from asyncio import TimeoutError
from discord.ext import commands
from helpers.akinator_helpers import AkinatorWrapper

class Aki(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['aki', 'tebakkarakter'])
    async def akinator(self, ctx):
        async with ctx.typing():
            aki = Akinator()
            wrapper = AkinatorWrapper()
            question = await aki.start_game(language='id')
            embed, components = wrapper.generate_embed(question=question, disable_components=False)
            game = await ctx.send(embed=embed, components=components)

        try:
            while aki.progression <= 80:
                btn = await game.wait_for('button', self.bot, by=ctx.author, timeout=60)
                await btn.respond(ninja_mode=True)

                if btn.custom_id == 'aki_yes': question = await aki.answer('yes')
                if btn.custom_id == 'aki_maybe': question = await aki.answer('probably')
                if btn.custom_id == 'aki_idk': question = await aki.answer('idk')
                if btn.custom_id == 'aki_no': question = await aki.answer('no')
                if btn.custom_id == 'aki_stop': raise TimeoutError('Player stopped the game')
                if aki.progression >= 80: break

                embed, components = wrapper.generate_embed(question=question, disable_components=False)
                await game.edit(embed=embed, components=components)
        except TimeoutError as e:
            message = 'Kamu menekan tombol stop' if str(e)=='Player stopped the game' else 'Hasbi terlalu lelah menunggu jawaban kamu'
            embed = wrapper.generate_error_embed(message=message)
        except AkiNoQuestions:
            embed = wrapper.generate_error_embed(message='Udah gak punya pertanyaan lagi maaf, kamu menang deh')

        async with ctx.typing():
            if aki.progression >= 80:
                await aki.win()
                guesses = aki.guesses
                index = 1
                embed, _ = wrapper.generate_embed(guess=guesses[index-1], guessing=True)

            await game.delete()
            await ctx.send(embed=embed)
            await aki.close()

def setup(bot):
    bot.add_cog(Aki(bot))