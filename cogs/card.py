import asyncio
from discord.ext import commands
from discord import Embed
from discord.ext.commands import Context
from configuration import BotInstance
import requests

deckAPI = "https://go-deck.harizmunawar.repl.co/deck"
currAPI = "https://robo-hasbi-currency-api.ganiyamustafa.repl.co"
bot = BotInstance.bot

class CardGame(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['bj'])
    async def blackjack(self, ctx:Context, bet:int):
        player = ctx.author
        player_curr = requests.get(currAPI+"/curr/"+str(player.id)).json()['data']['bal']
        if bet > int(player_curr):
            await ctx.send("Kamu gak punya uang sebanyak itu untuk dipakai berjudi")
            return
        
        player_hand = []
        dealer_hand = []
        deck_id, player_hand, dealer_hand = init_bj(player_hand, dealer_hand)
        
        initGame = Embed(color=0xecce8b)
        initGame.set_author(name=f"{player.name} Memulai Blackjack", icon_url=player.avatar_url)
        initGame.add_field(name=player.name, value=f"Cards - {' '.join(card_parser(player_hand))}\nScore - {score_counter(player_hand)}")
        initGame.add_field(name="Bang Hasbi", value=f"Cards - {card_parser(dealer_hand)[0]} ? \nScore - {score_counter(dealer_hand, 1)}")

        await ctx.send("Ketik h untuk hit, s untuk stand, atau a untuk akhiri permainan")
        await ctx.send(embed=initGame)

        try:
            finished = None
            while not finished:
                finished, game_embed = game_finished(player, player_hand, dealer_hand, bet)

                if not finished:
                    reply = await bot.wait_for('message', check=lambda m: (m.content.lower() in ['h', 's', 'a'] or m.content.lower().startswith('!bj')) and m.author == player, timeout=120)
                    message = reply.content.lower()

                    if message.startswith('!bj'):
                        await ctx.send("Anda masih memiliki game yang sedang berlangsung.")

                    if message == 'h':
                        player_hand = hit(deck_id, player_hand)
                        finished, game_embed = game_finished(player, player_hand, dealer_hand, bet)

                    if message in ['s', 'h']:
                        dealer_hand = dealer_ai(deck_id, dealer_hand)
                        finished, game_embed = game_finished(player, player_hand, dealer_hand, bet)

                    if message == 's':
                        finished, game_embed = game_finished(player, player_hand, dealer_hand, bet, True)

                    if message == 'a':
                        pass

                await ctx.send(embed=game_embed)

            winner, message = game_state(player, player_hand, dealer_hand)
            if winner == player.name:
                requests.post(currAPI+"/curr/add/"+str(player.id)+"/"+str(bet))
            elif winner == 'Bang Hasbi':
                requests.post(currAPI+"/curr/min/"+str(player.id)+"/"+str(bet))

        except asyncio.TimeoutError:
            await ctx.send(f"{player.name} tidak menjawab dalam 2 menit :(")

        requests.delete(deckAPI+"/"+str(deck_id))

def game_finished(player, player_hand, dealer_hand, bet, force_finished=False):
    winner, message = game_state(player, player_hand, dealer_hand)
    if (score_counter(player_hand) >= 21 or score_counter(dealer_hand) >= 21) or force_finished:
        game_embed = bj_embed(player, player_hand, dealer_hand, winner, bet, True, message)
        return True, game_embed
    
    game_embed = bj_embed(player, player_hand, dealer_hand, winner, bet, False, message)
    return False, game_embed

def bj_embed(player, player_hand, dealer_hand, winner, bet, finished, message=""):
    color = 0x00ff00 if winner == player.name else 0xff0000
    color = color if finished else 0xecce8b
    winner_name = player.name if winner == player.name else 'Bang Hasbi'

    game_embed = Embed(color=color)
    game_embed.set_author(name=f"{player.name} Memulai Blackjack", icon_url=player.avatar_url)

    if finished and winner == 'Draw':
        game_embed.add_field(name=f"Skor Seri!!! {message}", value="Tidak Ada Yang Harus Kehilangan Uang", inline=False)
    elif finished:
        finished_value = f"{player.name} Mendapat {bet}N$" if winner == player.name else f"{player.name} Harus Membayar {bet}N$"
        game_embed.add_field(name=f"{winner_name} Menang!!! {message}", value=finished_value, inline=False)

    game_embed.add_field(name=player.name, value=f"Cards - {' '.join(card_parser(player_hand))}\nScore - {score_counter(player_hand)}")

    if finished:
        game_embed.add_field(name="Bang Hasbi", value=f"Cards - {' '.join(card_parser(dealer_hand))}\nScore - {score_counter(dealer_hand)}")
    else:
        game_embed.add_field(name="Bang Hasbi", value=f"Cards - {card_parser(dealer_hand)[0]} ? \nScore - {score_counter(dealer_hand, 1)}")
    return game_embed

def init_bj(player_hand, dealer_hand):
    deck = requests.get(deckAPI+"/create?shuffle=true")

    if deck.status_code == 201:
        deckId = deck.json()['deckId']

        for i in range (0,2):
            draw = requests.get(deckAPI+"/"+str(deckId)+"/draw")
            if draw.status_code == 200:
                player_hand.append(draw.json()['card'])

        for i in range (0,2):
            draw = requests.get(deckAPI+"/"+str(deckId)+"/draw")
            if draw.status_code == 200:
                dealer_hand.append(draw.json()['card'])

    return deckId, player_hand, dealer_hand

def hit(deck_id, hand):
    draw = requests.get(deckAPI+"/"+str(deck_id)+"/draw")
    if draw.status_code == 200:
        hand.append(draw.json()['card'])

    return hand

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

def game_state(player, player_hand, dealer_hand):
    player_score = score_counter(player_hand)
    dealer_score = score_counter(dealer_hand)
    if player_score > 21: return 'Bang Hasbbi', 'Anda Busted'
    if dealer_score > 21: return player.name, 'Bang Hasbi Busted'
    if dealer_score == 21: return 'Bang Hasbi', 'Bang Hasbi Mendapat Blackjack'
    if player_score == 21: return player.name, 'Anda Mendapat Blackjack'
    if player_score > dealer_score and player_score < 21: return player.name, 'Skor Anda Lebih Besar Dari Bang Hasbi'
    if dealer_score > player_score and dealer_score < 21: return 'Dealer', 'Skor Bang Hasbi Lebih Besar Dari Anda'
    if dealer_score == player_score: return 'Draw', 'Skor Kalian Sama Ciee'

    return None, None
    
def dealer_ai(deck_id, dealer_hand):
    dealer_score, rank_list = score_counter(dealer_hand, with_rank=True)

    while dealer_score <= 16 or (dealer_score == 17 and 1 in rank_list):
        dealer_hand = hit(deck_id, dealer_hand)
        dealer_score = score_counter(dealer_hand)

    return dealer_hand


def setup(bot):
    bot.add_cog(CardGame(bot))
