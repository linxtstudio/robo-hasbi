from discord import Embed

class UI:
    # Emojis
    next_arrow = {'id': 885775938871263302, 'name': 'next_arrow', 'animated': False}
    previous_arrow = {'id': 885775975466553376, 'name': 'previous_arrow', 'animated': False}
    last_arrow = {'id': 885775836861575218, 'name': 'last_arrow', 'animated': False}
    first_arrow = {'id': 885775906629636116, 'name': 'first_arrow', 'animated': False}
    reply = {'id': 885797725327745085, 'name': 'reply', 'animated': False}

    # Embeds
    def error_embed(message):
        embed=Embed(color=0xd62929)
        embed.set_author(name=f"❌  {message}")
        return embed

    def success_embed(message):
        embed=Embed(color=0x58ee8a)
        embed.set_author(name=f"✅  {message}")
        return embed