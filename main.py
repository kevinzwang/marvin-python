import discord
from discord.ext import commands
import asyncio
import os
import sys
import time
from datetime import datetime

from classes.fileIO import FileIO

fio = FileIO()
bot = commands.Bot(command_prefix=commands.when_mentioned_or(fio.get('prefix')), pm_help=True)

async def _send(channel, message):
    if isinstance(channel, str):
        channel = discord.utils.get(server.channels, name=channel)
    await bot.send_message(channel, message)

async def _not_admin(ctx):
    await _send(ctx.message.channel, fio.get('messages', 'not-admin').format(ctx.message.author.mention))

async def _incorrect_usage(ctx):
    await _send(ctx.message.channel, fio.get('messages', 'incorrect-usage').format(ctx.message.author.mention, fio.get('prefix')))

@bot.event
async def on_ready():
    print('----------')
    print('Success! {} is connected!'.format(bot.user.name))
    print('ID: {}'.format(bot.user.id))
    print('TIME: {}'.format(time.ctime()))
    print('----------')

    global server 
    server = next(iter(bot.servers))

    await _send('logs', fio.get('messages', 'online'))

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
                await _send(message.channel, fio.get('messages', 'name-change').format(message.author.mention, fio.get('prefix')))
                break

    # jonnybot replacement
    if message.content.startswith('~') and server.get_member_named('JonnyBot#9936').status == discord.Status.offline:
        await bot.send_message(message.channel, fio.get('messages', 'jonnybot').format(server.get_member_named('JonnyBot#9936').mention, '😜'))

    await bot.process_commands(message)

def custom_get_prefix(message):
    if message.server == None:
        return ''
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
    t = round((datetime.utcnow() - ctx.message.timestamp).total_seconds() * 1000.0, 3) 
    await bot.reply(fio.get('messages', 'ping-pong').format(t))

@bot.command(pass_context=True)
async def opt(ctx, message: str):
    if message == 'in':
        fio.remove('opt-out',  str(ctx.message.author))
        await bot.reply(fio.get('messages', 'opt-in'))
    elif message == 'out':
        fio.add('opt-out',  str(ctx.message.author))
        await bot.reply(fio.get('messages', 'opt-out').format(fio.get('prefix')))
    else:
        await _incorrect_usage(ctx)

@bot.command()
async def xkcd(message: str):
    pass

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
async def prefix(ctx, *, message:str):
    message = message.split(' ')
    if message[0] == 'list':
        await bot.reply('the current prefix is `{}`'.format(fio.get('prefix')))
    elif message[0] == 'set' and message[1] != None:
        if fio.is_admin(ctx.message.author):
            fio.set('prefix', message[1])
            bot.command_prefix=commands.when_mentioned_or(fio.get('prefix'))
            await bot.reply('prefix set successfully to `{}`'.format(message[1]))
        else:
            await _incorrect_usage(ctx)
    else:
        await _incorrect_usage(ctx)

@bot.command(pass_context=True)
async def quit(ctx, *, message:str=None):
    if fio.is_admin(ctx.message.author):
        await bot.say('Bye... 😞')
        await _send(fio.get('channels', 'log'), 'Quitting... bye 😞')
        if message != 'no-dump':
            fio.dump()
        await bot.logout()
    else:
        await _not_admin(ctx)

@bot.command(pass_context=True)
async def restart(ctx, *, message: str=None):
    if fio.is_admin(ctx.message.author):
        await bot.say('brb')
        await _send(fio.get('channels', 'log'), 'Restarting, brb.')
        if message != 'no-dump':
            fio.dump()
        bot.logout()
        os.execl(sys.executable, sys.executable, * sys.argv)
    else:
        await _not_admin(ctx)

@bot.command(pass_context=True)
async def dump(ctx):
    if fio.is_admin(ctx.message.author):
        await bot.say('dumping data...')
        fio.dump()
        await bot.say('done!')
    else:
        await _not_admin(ctx)

bot.run(fio.get('token'))