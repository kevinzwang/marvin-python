import asyncio
import discord
from discord.ext import commands
from classes import fileIO

class Bot(commands.Bot):
    def __init__(self):
        self.disabled = []
        super().__init__(command_prefix=commands.when_mentioned_or(fileIO.get('config', 'prefix')), pm_help=True)

    async def _get_prefix(self, message):
        if message.server == None:
            return ''
        else:
            return list(fileIO.get('config', 'prefix')) + [message.server.me.mention, 'marv ', 'marv, ', 'Marv ', 'Marv, ']

    async def send_message(self, channel, *args, **kwargs):
        if isinstance(channel, str):
            channel = discord.utils.get(next(iter(self.servers)).channels, name=channel)
        return await super().send_message(channel, *args, **kwargs)

    async def process_commands(self, message):
        for cmdName in self.disabled:
            prefixes = await self._get_prefix(message)
            for prefix in prefixes:
                if message.content.startswith(prefix + cmdName):
                    await self.send_message(message.channel, message.author.mention + ', that command is disabled!')
                    return
        
        await super().process_commands(message)