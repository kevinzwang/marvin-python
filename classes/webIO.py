import asyncio
import aiohttp
from io import BytesIO
from html2text import html2text

def __init__():
    global session
    session = aiohttp.ClientSession()

async def lmgtfy(message):
    params = {'q': message}
    response = await session.get(url='https://lmgtfy.com/', params=params)
    return str(response.url)

async def xkcdLinks(message):
    params = {'q': message}
    response = await session.get(url='http://apps.reddolution.com/RelevantXKCD/', params=params)
    html = await response.text()

    relevants = []
    toFind = 'http://xkcd.com/'

    fromIndex = html.find(toFind) + len(toFind)
    for i in range(0, 5):
        start = html.find(toFind, fromIndex)
        end = html.find('"', start)
        relevants.append(html[start:end])
        fromIndex = end

    return relevants

async def xkcdContent(url):
    response = await session.get(url=url)
    html = await response.text()

    async def getTitle():
        start = html.find('ctitle') + len('ctitle') + 2
        end = html.find('<', start)
        return html2text(html[start:end])[:-2]

    async def getNumber():
        toFind = 'Permanent link to this comic: https://xkcd.com/'
        start = html.find(toFind) + len(toFind)
        end = html.find('/', start)
        return html[start:end]

    async def getImage():
        start = html.find('imgs.xkcd.com')
        end = html.find('"', start)
        
        imgResp = await session.get(url='http://' + html[start:end])
        my_bytes = await imgResp.read()
        return BytesIO(my_bytes)

    async def getHover():
        start = html.find('"', html.find('imgs.xkcd.com')) + 9
        end = html.find('"', start)
        return html2text(html[start:end])[:-2]

    title = await getTitle()
    number = await getNumber()
    image = await getImage()
    hover = await getHover()
    return (title, number, image, hover)