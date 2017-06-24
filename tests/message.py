import discord
import asyncio
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))
from classes.fileIO import FileIO

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    if message.content.startswith('~'):
        await client.send_message(message.channel, 'F*** you I\'m not jonnybot')
    elif "are you sure about that" in message.content or "aysat" in message.content:
        await client.send_message(message.channel, 'Good question.')
    elif "hangouts" in message.content:
        await client.send_message(message.channel, '#discordmasterrace')
    elif message.content.startswith('!quit'):
        await client.send_message(message.channel, 'Bye... ;(')
        await client.logout()

client.run(FileIO().get('token'))