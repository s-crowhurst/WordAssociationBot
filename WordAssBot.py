import discord
import random
import os
from dataclasses import dataclass

@dataclass
class Bot:
    """ Establishes a generic Discord Bot

    Keyword arguments:
    name -- Give the bot a name!
    startup_message -- The message displayed in chat when the bot starts
    token -- The secret token used identification and authentication
    intents -- Sets which events the bot can respond to (e.g. DM's)
    client -- Initialises the discord client with params
    """
    name: str = "UnnamedBot"
    startup_message: str = "Bot ready for action!"
    prompt_message: str = " it's your turn!"
    token: str = os.environ['BOT_TOKEN']
    channel: int = 0
    guild: int = 0
    intents: discord.flags.Intents = discord.flags.Intents.all()
    client: discord.client.Client = discord.Client(intents=intents)

WordAssBot = Bot(startup_message="Word Ass(ociation) Bot ready for action!",
                 channel = 1099837114004291645,
                 guild = 1099378991753871430
                 )

# Event listener for when the bot is ready
@WordAssBot.client.event
async def on_ready():
    """ Sends the startup message to the specified channel
    """
    print(f'Logged in as {WordAssBot.client.user}')
    await WordAssBot.client.get_channel(WordAssBot.channel).send(Bot.startup_message)

# Event listener for when a message is sent
@WordAssBot.client.event
async def on_message(message):
    members = [member for member in message.guild.members if member != WordAssBot.client.user]
    if message.author == WordAssBot.client.user:
        return
    elif message.channel.id == WordAssBot.channel:
        random_member = random.choice(members)
        await message.channel.send(random_member.mention + WordAssBot.prompt_message)

# Run the Bot
WordAssBot.client.run(WordAssBot.token)
