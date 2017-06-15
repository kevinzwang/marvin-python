import discord
import asyncio
import io
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))
import fileIO

client = discord.Client()

@client.event
async def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('------')

@client.event
async def on_message(message):
	if message.content.startswith('!test'):
		await client.send_message(message.channel, 'hey this works')

client.run(fileIO.getToken())