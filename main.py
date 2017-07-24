import asyncio
import os
import sys
import time
from datetime import datetime

import discord
from discord.ext import commands

from classes import fileIO
from classes import webIO
from classes import marvin

fileIO.__init__()
webIO.__init__()
bot = marvin.Bot()
loop = asyncio.get_event_loop()
availables = {}

async def _not_admin(ctx):
    await bot.send_message(ctx.message.channel, fileIO.get('messages', 'not-admin').format(ctx.message.author.mention))

async def _incorrect_usage(ctx):
    await bot.send_message(ctx.message.channel, fileIO.get('messages', 'incorrect-usage').format(ctx.message.author.mention, fileIO.get('config', 'prefix')))

@bot.event
async def on_ready():
    print('----------')
    print('Success! {} is connected!'.format(bot.user.name))
    print('ID: {}'.format(bot.user.id))
    print('TIME: {}'.format(time.ctime()))
    print('----------')

    global server
    server = next(iter(bot.servers))

# CUSTOM ACTIONS

@bot.event
async def on_message(message):
    lower = message.content.lower()

    # change nickname when people say "I'm ___"
    if str(message.author) not in fileIO.get('config', 'opt-out') and not message.author.bot:
        for im in ['im ', 'i\'m ', 'i am ']:
            index = lower.find(im)
            if index != -1 and (index == 0 or lower[index - 1] == ' '):
                punctuation = len(lower)
                for p in ['.', ',', ';', '!', '?']:
                    i = message.content.find(p, index)
                    if i != -1  and i < punctuation:
                        punctuation = i

                nickname = message.content[index + len(im):punctuation]

                if len(nickname) > 32:
                    nickname = nickname[:33]
                    nickname = nickname[:nickname.rfind(' ')]

                oldName = message.author.nick
                await bot.send_message(message.channel, fileIO.get('messages', 'name-change').format(nickname, fileIO.get('config', 'prefix')))
                await bot.change_nickname(message.author, nickname)
                await asyncio.sleep(30)
                await bot.change_nickname(message.author, oldName)
                break

    # jonnybot replacement
    if message.content.startswith('~') and server.get_member_named('JonnyBot#9936').status == discord.Status.offline:
        await bot.send_message(message.channel, fileIO.get('messages', 'jonnybot').format(server.get_member_named('JonnyBot#9936').mention, '😜'))

    await bot.process_commands(message)

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

@bot.command()
async def lmgtfy(*, message: str):
    url = await webIO.lmgtfy(message)
    await bot.say(url)

@bot.command(pass_context=True)
async def ping(ctx):
    t = round((datetime.utcnow() - ctx.message.timestamp).total_seconds() * 1000.0, 3) 
    await bot.reply(fileIO.get('messages', 'ping-pong').format(t))

@bot.command(pass_context=True)
async def opt(ctx, message: str):
    if message == 'in':
        fileIO.remove('config', 'opt-out',  str(ctx.message.author))
        await bot.reply(fileIO.get('messages', 'opt-in'))
    elif message == 'out':
        fileIO.add('config', 'opt-out',  str(ctx.message.author))
        await bot.reply(fileIO.get('messages', 'opt-out').format(fileIO.get('config', 'prefix')))
    else:
        await _incorrect_usage(ctx)

@bot.command(pass_context=True) 
async def available(ctx, message: str):
    if message == 'list':
        if len(availables) > 0:
            await bot.reply('people currently available:')
            for member in availables:
                nick = member.nick
                if nick == None:
                    nick = member.name
                await bot.send_message(ctx.message.channel, ' - ' + nick)
        else:
            await bot.reply('nobody currently available. :cry:')
    elif message == 'remove':
        del availables[ctx.message.author]
        await bot.reply('success!')
    elif message.isdigit():
        if ctx.message.author in availables:
            availables[ctx.message.author] += 1
        else:
            availables[ctx.message.author] = 1

        mentions = ''
        if len(availables) >= 4:
            for member in availables:
                mentions += member.mention + ' '
            await bot.send_message('game-night', '{}, there\'s enough people for @game-night!'.format(mentions))
        else:
            await bot.reply('availability recorded successfully!')

        await asyncio.sleep(int(message)*60)
        if ctx.message.author in availables.keys():
            availables[ctx.message.author] -= 1
            if availables[ctx.message.author] == 0:
                del availables[ctx.message.author]
    else:
        await _incorrect_usage(ctx)

@bot.command(pass_context=True) 
async def avail(ctx, message: str):
    await ctx.invoke(available, message)

@bot.command(pass_context=True)
async def xkcd(ctx, *, message:str=None):
    try:
        if message == 'latest' or message == None:
            content = await webIO.xkcdContent('https://xkcd.com/')

            top = content[0].upper() + ' (' + content[1] + ')'
            bottom = '*' + content[3] + '*'

            await bot.send_file(ctx.message.channel, content[2], filename='xkcd.png', content=top)
            await bot.say(bottom)

        elif message == 'random':
            content = await webIO.xkcdContent('https://c.xkcd.com/random/comic/')

            top = content[0].upper() + ' (' + content[1] + ')'
            bottom = '*' + content[3] + '*'

            await bot.send_file(ctx.message.channel, content[2], filename='xkcd.png', content=top)
            await bot.say(bottom)

        else:
            links = await webIO.xkcdLinks(message)
            currentComic = 0

            correct = False
            
            response = None

            while not correct:
                content = await webIO.xkcdContent(links[currentComic])

                top = content[0].upper() + ' (' + content[1] + ')'
                bottom = '*' + content[3] + '*'

                r1 = await bot.send_file(ctx.message.channel, content[2], filename='xkcd.png', content=top)
                r2 = await bot.say(bottom)
                
                await bot.add_reaction(r2, '✅')
                await bot.add_reaction(r2, '⛔')

                reaction = await bot.wait_for_reaction(emoji=['✅', '⛔'], message=r2, timeout=30, user=ctx.message.author)

                if reaction == None:
                    await bot.remove_reaction(r2, '✅', bot.user)
                    await bot.remove_reaction(r2, '⛔', bot.user)
                    correct = True
                elif str(reaction.reaction.emoji) == '✅':
                    await bot.remove_reaction(r2, '✅', bot.user)
                    await bot.remove_reaction(r2, '⛔', bot.user)
                    await bot.remove_reaction(r2, '✅', ctx.message.author)
                    correct = True
                elif str(reaction.reaction.emoji) == '⛔':
                    if currentComic < 4:
                        await bot.delete_message(r1)
                        await bot.delete_message(r2)
                    else:
                        await bot.delete_message(r1)
                        await bot.delete_message(r2)
                        await bot.say('Welp, that\'s all. Better luck next time.')
                        correct = True

                    currentComic += 1
    except Exception:
        await bot.say('Whoops, something went wrong while trying to get your xkcd. Try again later.')

# TORD

async def tord(mode, ctx, message):
    if message == None:
        await bot.send_message(ctx.message.channel, fileIO.get_tord(mode))
    elif message == 'list':
        await bot.send_message(ctx.message.author, fileIO.list_tord(mode))
    else:
        _incorrect_usage(ctx)

@bot.command(pass_context=True)
async def truth(ctx, *, message:str=None):
    await tord('truth', ctx, message)

@bot.command(pass_context=True)
async def dare(ctx, *, message:str=None):
    await tord('dare', ctx, message)

@bot.command(pass_context=True)
async def wyr(ctx, *, message:str=None):
    await tord('wyr', ctx, message)

# SYSTEM

@bot.command(pass_context=True)
async def prefix(ctx, *, message:str):
    message = message.split(' ')
    if message[0] == 'list':
        await bot.reply('the current prefix is `{}`'.format(fileIO.get('config', 'prefix')))
    elif message[0] == 'set' and message[1] != None:
        if fileIO.is_admin(ctx.message.author):
            fileIO.set('config', 'prefix', message[1])
            bot.command_prefix=commands.when_mentioned_or(fileIO.get('config', 'prefix'))
            await bot.reply('prefix set successfully to `{}`'.format(message[1]))
        else:
            await _incorrect_usage(ctx)
    else:
        await _incorrect_usage(ctx)

@bot.command(pass_context=True)
async def quit(ctx, *, message:str=None):
    if fileIO.is_admin(ctx.message.author):
        await bot.say('Bye... 😞')
        if message != 'no-dump':
            fileIO.dump()
        await bot.logout()
    else:
        await _not_admin(ctx)

@bot.command(pass_context=True)
async def restart(ctx, *, message: str=None):
    if fileIO.is_admin(ctx.message.author):
        await bot.say('brb')
        if message != 'no-dump':
            fileIO.dump()
        bot.logout()
        os.execl(sys.executable, sys.executable, * sys.argv)
    else:
        await _not_admin(ctx)

@bot.command(pass_context=True)
async def dump(ctx):
    if fileIO.is_admin(ctx.message.author):
        await bot.say('dumping data...')
        fileIO.dump()
        await bot.say('done!')
    else:
        await _not_admin(ctx)

if fileIO.get('config', 'token') == None:
    print('Before we proceed, you must supply the bot token in \'yaml/config.yaml\'. Quitting...')
else:
    bot.run(fileIO.get('config', 'token'))