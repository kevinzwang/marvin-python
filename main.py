import discord
from discord.ext import commands
import asyncio
import os
import sys
import time
import datetime

from classes.fileIO import FileIO

fio = FileIO()
bot = commands.Bot(command_prefix=commands.when_mentioned_or(fio.get('default-prefix', default='!')))

@bot.event
async def on_ready():
    print('----------')
    print('Success! {} is connected!'.format(bot.user.name))
    print('ID: {}'.format(bot.user.id))
    print('SERVERS:')
    for s in bot.servers:
    	print(' - {}'.format(s.name))
    print('----------')


# CUSTOM ACTIONS

@bot.event
async def on_message(message):
    lower = message.content.lower()

    # change nickname when people say "I'm ____"
    if not fio.contains('opt-out', str(message.author)):
        for im in ['im ', 'i\'m ', 'i am ']:
            if im in lower:
                index = lower.find(im) + len(im)
                nickname = message.content[index:]
                if len(nickname) > 32:
                    nickname = nickname[:33]
                    nickname = nickname[:nickname.rfind(' ')]

                await bot.change_nickname(message.author, nickname)
                await bot.send_message(message.channel, 'Hi, {}!'.format(message.author.mention))
                await bot.send_message(message.channel, '*(Type \'{}opt out\' if you would like to opt out of the fun)*'.format(fio.get('default-prefix')))
                break

    # jonnybot replacement
    if message.content.startswith('~') and message.server.get_member_named('JonnyBot#9936').status == discord.Status.offline:
        await bot.send_message(message.channel, 'Sorry, but {} is not online right now. Wanna give me a try instead? 😜'.format(message.server.get_member_named('JonnyBot#9936').mention))

    await bot.process_commands(message)

def custom_get_prefix(message):
    if message.server == None:
        return ''
    elif fio.get('servers', message.server.name, 'prefix') != None:
        return [fio.get('servers', message.server.name, 'prefix'), bot.user.mention + ' ']
    else:
        prefix = bot.command_prefix
        if callable(prefix):
            ret = prefix(bot, message)
            if asyncio.iscoroutine(ret):
                ret = yield from ret
            return ret
        else:
            return prefix

bot._get_prefix = custom_get_prefix

@bot.event
async def on_reaction_add(reaction, user):
    # pin item
    if reaction.emoji == '📌':
        await bot.pin_message(reaction.message)

@bot.event
async def on_reaction_remove(reaction, user):
    # unpin item
    if reaction.emoji == '📌':
        await bot.unpin_message(reaction.message)

# COMMANDS

@bot.command(pass_context=True)
async def ping(ctx):
    t = round((datetime.datetime.utcnow() - ctx.message.timestamp).total_seconds() * 1000.0, 3) 
    await bot.reply('Pong!\nThat took {} milliseconds.'.format(t))

@bot.command(pass_context=True)
async def opt(ctx, message: str):
    if message == 'in':
        fio.remove('opt-out',  str(ctx.message.author))
        await bot.reply('opted in successfully!')
    elif message == 'out':
        fio.add('opt-out',  str(ctx.message.author))
        await bot.reply('opted out successfully. If you would like to rejoin the fun, just do \'{}opt in\''.format(fio.get('default-prefix')))
    else:
        await bot.reply('incorrect usage. Say either \'{0}opt in\' or \'{0}opt out\''.format(fio.get('default-prefix')))

@bot.command()
async def xkcd(message: str):
    

# TORD

@bot.command()
async def truth():
    await bot.say(fio.get_tord('truth'))

@bot.command()
async def dare():
    await bot.say(fio.get_tord('dare'))

@bot.command()
async def wyr():
    await bot.say(fio.get_tord('wyr'))

# SYSTEM

@bot.command(pass_context=True)
async def server_prefix(ctx, message: str):
    if not ctx.message.server:
        await bot.reply('bruh this is not a server, this is a DM. You don\'t have to use prefixes here.')
    elif not fio.is_admin(ctx.message.server, ctx.message.author):
        await bot.reply('you do not have administrative privileges!')
    else:
        fio.set('servers', ctx.message.server.name, 'prefix', message)
        await bot.reply('server prefix set successfully to `{}`!'.format(message))

@bot.command(pass_context=True)
async def global_prefix(ctx, message: str):
    if str(ctx.message.author) in fio.get('global-admin'):
        fio.set('global-prefix', message)
        await bot.reply('global prefix set successfully to {}!'.format(message))
    else:
        await bot.reply('you do not have administrative privileges!')

@bot.command(pass_context=True)
async def quit(ctx):
    if fio.is_admin(ctx.message.server, ctx.message.author):
        await bot.say('Bye... ;(')
        fio.dump()
        await bot.logout()
    else:
        await bot.reply('you do not have administrative privileges!')

@bot.command(pass_context=True)
async def restart(ctx, *message: str):
    if fio.is_admin(ctx.message.server, ctx.message.author):
        await bot.say('brb')
        if message != 'no-dump':
            fio.dump()
        bot.logout()
        os.execl(sys.executable, sys.executable, * sys.argv)

bot.run(fio.get('token'))