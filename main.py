import discord
from discord.ext import commands
import asyncio
import os
import time
import datetime

from classes.fileIO import FileIO

fio = FileIO()
bot = commands.Bot(command_prefix=fio.get('default-prefix', '!'))

@bot.event
async def on_ready():
    print('Yay! {} is connected!'.format(bot.user.name))
    print('ID: {}'.format(bot.user.id))
    print('SERVERS:')
    for s in bot.servers:
    	print(' - {}'.format(s.name))
    print('------')

@bot.event
async def on_message(message):
    m = message.content.lower()
    if not fio.contains('opt-out', str(message.author)):
        for im in ['im ', 'i\'m ', 'i am ']:
            if im in m:
                index = m.find(im) + len(im)
                nickname = message.content[index:]
                if len(nickname) > 32:
                    nickname = nickname[:33]
                    nickname = nickname[:nickname.rfind(' ')]

                await bot.change_nickname(message.author, nickname)
                await bot.send_message(message.channel, 'Hi, {}!'.format(message.author.mention))
                if not fio.contains('opt-in', str(message.author)):
                    await bot.send_message(message.channel, '*(\'{}opt out\' if you would like to opt out of the fun)*'.format(fio.get('default-prefix')))
                    fio.add('opt-in', str(message.author))
                break


    await bot.process_commands(message)

@bot.command(pass_context=True)
async def ping(ctx):
    t = (datetime.datetime.utcnow() - ctx.message.timestamp).total_seconds()
    await bot.reply('Pong!\nThat took {} seconds.'.format(t))

@bot.command(pass_context=True)
async def quit(ctx):
    await bot.say('Bye... ;(')
    fio.dump()
    await bot.logout()

@bot.command(pass_context=True)
async def opt(ctx, message: str):
    if message == 'in':
        fio.add('opt-in', str(ctx.message.author))
        fio.remove('opt-out',  str(ctx.message.author))
        await bot.reply('opted in successfully!')
    elif message == 'out':
        fio.add('opt-out',  str(ctx.message.author))
        fio.remove('opt-in', str(ctx.message.author))
        await bot.reply('opted out successfully. If you would like to rejoin the fun, just do \'{}opt in\''.format(fio.get('default-prefix')))
    else:
        await bot.reply('incorrect usage. Say either \'{0}opt in\' or \'{0}opt out\''.format(fio.get('default-prefix')))

bot.run(fio.get('token'))