import asyncio
from discord.ext import commands
from discord import Embed
from discord.ext.commands import Context
from configuration import BotInstance
import requests

# deckAPI = "https://go-deck.harizmunawar.repl.co/deck"
deckAPI = "http://localhost:8000"
currAPI = "https://robo-hasbi-currency-api.ganiyamustafa.repl.co"
bot = BotInstance.bot

class CardGame(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['bj'])
    async def blackjack(self, ctx:Context, bet:int):
        player = ctx.author
        player_curr = requests.get(currAPI+"/curr/"+str(player.id))
        if player_curr.status_code == 404:
            await ctx.send(embed=Embed().add_field(name="Tidak Dapat Memulai Game Blackjack", value="Sepertinya Anda Belum Terdaftar Di Dalam Database Kami, Ketik !regis Untuk Mendaftarkan Diri"))
            return
        if bet > int(player_curr.json()['data']['bal']):
            await ctx.send(embed=Embed().add_field(name="Tidak Dapat Memulai Game Blackjack", value="Anda Tidak Punya Uang Sebanyak Itu Untuk Digunakan Berjudi"))
            return
        

        # Create new blackjack game
        game = requests.get(deckAPI+"/blackjack/create")
        if not game.status_code == 201:
            await ctx.send(embed=Embed().add_field(name="Tidak Dapat Memulai Game Blackjack", value="Terjadi Kesalahan Saat Mencoba Membuat Game"))
            return

        game = game.json()["blackjack"]
        game_id = game["id"]
        player_hand = [card for card in game["playerHand"]]
        dealer_hand = [card for card in game["dealerHand"]]
        winner = game["winner"]
        finished = game["finished"]
    
        await ctx.send(embed=bj_embed(player, player_hand, dealer_hand, winner, bet, finished))

        try:
            while not finished:
                status = requests.get(deckAPI+"/blackjack/"+str(game_id)+"/status").json()["blackjack"]

                if not status["finished"]:
                    reply = await bot.wait_for('message', check=lambda m: (m.content.lower() in ['h', 's', 'a'] or m.content.lower().startswith('!bj')) and m.author == player, timeout=120)
                    message = reply.content.lower()

                    if message.startswith('!bj'):
                        await ctx.send("Anda masih memiliki game yang sedang berlangsung.")

                    if message == 'h':
                        requests.get(deckAPI+"/blackjack/"+str(game_id)+"/hit")
                        requests.get(deckAPI+"/blackjack/"+str(game_id)+"/dealer-ai")
                        status = requests.get(deckAPI+"/blackjack/"+str(game_id)+"/status").json()["blackjack"]

                    if message == 's':
                        requests.get(deckAPI+"/blackjack/"+str(game_id)+"/dealer-ai?stand=true")
                        status = requests.get(deckAPI+"/blackjack/"+str(game_id)+"/status").json()["blackjack"]

                    if message == 'a':
                        finished = True
                        game_embed = Embed(color=0xff0000).add_field(name="Permainan Dihentikan", value=f"{player.name} Harus Membayar {bet/2}N$")
                        requests.post(currAPI+"/curr/add/"+str(player.id)+"/"+str((bet/2)))

                player_hand = [card for card in status["playerHand"]]
                dealer_hand = [card for card in status["dealerHand"]]
                winner = status["winner"]
                message = status["message"]
                finished = status["finished"]
                
                if not message == 'a': game_embed = bj_embed(player, player_hand, dealer_hand, winner, bet, finished, message)

                await ctx.send(embed=game_embed)

            if winner == "Player":
                requests.post(currAPI+"/curr/add/"+str(player.id)+"/"+str(bet))
            elif winner == 'Dealer':
                requests.post(currAPI+"/curr/min/"+str(player.id)+"/"+str(bet))

        except asyncio.TimeoutError:
            await ctx.send(f"{player.name} tidak menjawab dalam 2 menit :(")

        requests.delete(deckAPI+"/deck/"+str(game["deckId"]))

def bj_embed(player, player_hand, dealer_hand, winner, bet, finished, message=""):
    color = 0x00ff00 if winner == "Player" else 0xff0000
    color = color if finished else 0xecce8b
    winner_name = player.name if winner == "Player" else 'Bang Hasbi'

    game_embed = Embed(color=color)
    game_embed.set_author(name=f"{player.name} Memulai Blackjack", icon_url=player.avatar_url)
    game_embed.set_footer(text='Ketik h untuk hit, s untuk stand, atau a untuk akhiri permainan')

    if finished and winner == 'Draw':
        game_embed.add_field(name=f"Skor Seri!!! {message}", value="Tidak Ada Yang Harus Kehilangan Uang", inline=False)
    elif finished:
        finished_value = f"{player.name} Mendapat {bet}N$" if winner == "Player" else f"{player.name} Harus Membayar {bet}N$"
        game_embed.add_field(name=f"{winner_name} Menang!!! {message}", value=finished_value, inline=False)

    game_embed.add_field(name=player.name, value=f"Cards - {' '.join(card_parser(player_hand))}\nScore - {score_counter(player_hand)}")

    if finished:
        game_embed.add_field(name="Bang Hasbi", value=f"Cards - {' '.join(card_parser(dealer_hand))}\nScore - {score_counter(dealer_hand)}")
        return game_embed
    
    return game_embed.add_field(name="Bang Hasbi", value=f"Cards - {card_parser(dealer_hand)[0]} ? \nScore - {score_counter(dealer_hand, 1)}")

def card_parser(list_card):
    suit_symbols = ['♠', '♦', '♣', '♥']
    rank_verbose = ['-', 'A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'Joker']

    return [f"{rank_verbose[card['rank']]} {suit_symbols[card['suit']]}" for card in list_card]

def score_counter(list_card, n=None, with_rank=False):
    score_list = [0, 11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
    rank_list = []
    score = 0
    i = 0
    for card in list_card:
        if n and i == n: break
        score += score_list[card['rank']]
        rank_list.append(card['rank'])
        i += 1

    if score > 21 and 1 in rank_list:
        score -= 10

    if with_rank: return score, rank_list

    return score

def setup(bot):
    bot.add_cog(CardGame(bot))
