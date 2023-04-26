import discord
import random
import os
import re
import asyncio
from dataclasses import dataclass

# --- Bot Options ---

@dataclass
class Bot:
    """ Establishes a generic Discord Bot
    Keyword arguments:
    startup_message -- The message displayed in chat when the bot starts
    token -- The secret token used identification and authentication
    intents -- Sets which events the bot can respond to (e.g. DM's)
    client -- Initialises the discord client with params
    """
    startup_message: str = "Bot ready for action!"
    token: str = ""
    channel: int = 0
    guild: int = 0
    intents: discord.flags.Intents = discord.flags.Intents.all()
    client: discord.client.Client = discord.Client(intents=intents)
    current_player: discord.member.Member = None
    next_player: discord.member.Member = None
    members: discord.member.Member = None

    def run(self):
        self.client.run(self.token)


@dataclass
class WordAssociationBot(Bot):

    def prompt_message(name):
        return f"It's your turn @{name.mention}!"

    def not_your_turn(name):
        return f"It is not your turn!"

    def one_word_warning(name):
        return f"Stick to just one word please!"

WordAssBot = WordAssociationBot(channel=1099739317917712474,
                                guild=1099378991753871430,
                                token= os.environ['BOT_TOKEN']
                                )

def Choose_New_Player():
    if WordAssBot.current_player == None:
            WordAssBot.current_player = random.choice(WordAssBot.members)
    else:
        while True:
            next_player = random.choice(WordAssBot.members)
            if (next_player != WordAssBot.current_player) or (len(WordAssBot.members)==1):
                WordAssBot.current_player = next_player
                return


# --- EVENT LISTNERS ---

# Event listener for when the bot is ready
@WordAssBot.client.event
async def on_ready():
    """ Sends the startup message to the specified channel
    """
    print(f'Logged in as {WordAssBot.client.user}')
    await WordAssBot.client.get_channel(WordAssBot.channel).send(Bot.startup_message)
    Choose_New_Player()
    await WordAssBot.client.get_channel(WordAssBot.channel).send(WordAssBot.current_player.mention)

# Event listener for when a message is sent
@WordAssBot.client.event
async def on_message(message):
    #print([member for member in message.guild.members if member != WordAssBot.client.user])
    WordAssBot.members = [member for member in message.guild.members if (member != WordAssBot.client.user and member.name != "random.bot")]
    if message.author == WordAssBot.client.user:
        return
    elif message.channel.id == WordAssBot.channel:
        Choose_New_Player()
        await message.channel.send(WordAssBot.current_player.mention)


# --- Program Start ---

WordAssBot.run()  # Run the bot!
