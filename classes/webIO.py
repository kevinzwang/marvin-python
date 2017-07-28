import asyncio
import aiohttp
from io import BytesIO
from bs4 import BeautifulSoup

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
    soup = BeautifulSoup(html, 'html.parser')

    relevants = []

    for i in range (1, 6):
        div = soup.find('div', id='best' + str(i))
        link = div.h3.a
        relevants.append(link['href'])

    return relevants

async def xkcdContent(url):
    response = await session.get(url=url)
    html = await response.text()
    soup = BeautifulSoup(html, 'html.parser')
    content = soup.find('div', id='middleContainer')

    async def getTitle():
        return soup.find(id='ctitle').string

    async def getNumber():
        toFind = 'Permanent link to this comic: https://xkcd.com/'
        tag = str(content)
        start = tag.find(toFind) + len(toFind)
        end = tag.find('/', start)
        return tag[start:end]

    async def getImage():
        link = content.find('div', id='comic').img['src']
        
        return 'http://' + link[2:]

    async def getHover():
        return content.find('div', id='comic').img['title']

    title = await getTitle()
    number = await getNumber()
    image = await getImage()
    hover = await getHover()
    return (title, number, image, hover)