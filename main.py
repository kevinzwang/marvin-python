import discord
import asyncio
import os
import fileIO

bot = discord.Client()

@bot.event
async def on_ready():
    print('Yay! {} is connected!'.format(bot.user.name))
    print('ID: {}'.format(bot.user.id))
    print('SERVERS:')
    for s in bot.servers:
    	print('\t{}'.format(s.name))
    print('------')
    
bot.run(fileIO.getToken())