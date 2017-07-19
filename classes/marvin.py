import asyncio
import discord
from discord.ext import commands
from classes import fileIO

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned_or(fileIO.get('config', 'prefix')), pm_help=True)

    async def _get_prefix(self, message):
        if message.server == None:
            return ''
        else:
            return list(fileIO.get('config', 'prefix')) + [message.server.me.mention, 'marv ', 'marv, ', 'Marv ', 'Marv, ']

    async def send_message(self, channel, message):
        if isinstance(channel, str):
            channel = discord.utils.get(next(iter(self.servers)).channels, name=channel)
        await super().send_message(channel, message)